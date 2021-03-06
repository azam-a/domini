import datetime
import logging
import os
import re

from flask import Flask, render_template, request

import controllers

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
app.config["GA_TRACKING_ID"] = os.environ["GA_TRACKING_ID"]

URL_PATTERN = (r"https:\/\/api.dominos.com.my\/api\/GPSTracker\/CartId\/\d+")


@app.route("/", methods=["GET"])
def index():
    return render_template("intro.html")


@app.route("/how-to", methods=["GET"])
def how_to():
    return render_template("how_to.html")


@app.route("/add-form", methods=["GET"])
def add_form():
    return render_template("add_form.html")


@app.route("/add-post", methods=["POST"])
def add_post():
    try:
        data = request.form
        controller = controllers.ItemController()
        if is_valid_url(data["url"]):
            controller.add(data["url"], data["token"], data["phone"])
            return render_template("base.html", text_only="great success!")

        else:
            return render_template("base.html", text_only="failed :'(")

    except Exception:
        return render_template("base.html", text_only="failed :'(")


def is_valid_url(url, pattern=URL_PATTERN):
    return bool(re.match(pattern, url))


def scheduled():
    mystring = (f"schedule triggered on {datetime.datetime.utcnow()}")
    logger.info(mystring)

    controller = controllers.ItemController()
    items = controller.get_active_items()
    logger.info(f"processing {len(items)} items")
    controller.process_items(items)

    return mystring


if __name__ == "__main__":
    app.run()
