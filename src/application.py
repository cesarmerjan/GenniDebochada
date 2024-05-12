import functools
import time
from collections import defaultdict

from flask import Flask, render_template, request, send_file
from flask_cors import CORS, cross_origin

import src.services as services

application = Flask(__name__, static_url_path="/static")
CORS(application)
RATE_LIMITING = defaultdict(int)


def check_rate_limit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ip = request.remote_addr

        if ip in RATE_LIMITING:
            if (RATE_LIMITING[ip] - time.time()) < 60:
                return {"message": "Too Many Requests"}, 429
            else:
                RATE_LIMITING[ip] = time.time()
        else:
            RATE_LIMITING[ip] = time.time()

        return func(*args, **kwargs)

    return wrapper


@application.get("/")
def index():
    return render_template("index.html", music="/audios/piada.mp3")


@application.get("/make-a-joke/<topic>")
@check_rate_limit
@cross_origin()
def make_a_joke(topic):

    if not topic:
        return {"message": "missing the topic of the personality"}, 400

    try:
        services.validate_topic(topic)
    except services.TopicNotAllowed:
        return {"message": "invalid topic"}, 400
    try:
        text = services.generate_joke(topic)
        audio = services.text_to_speech(text)
        return send_file(audio, mimetype="audios/mp3", as_attachment=False)
    except Exception:
        return {"message": "Internal Server Error"}, 500
