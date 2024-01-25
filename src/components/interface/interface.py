from flask import Flask, render_template, request

from config.config import Config
from src.utils import get_ip


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            Config.set_name(request.form["text"])
        return render_template("index.html")

    return app

def run():
    app = create_app()
    app.run(host=str(get_ip()), port=5000)