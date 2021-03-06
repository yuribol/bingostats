import os
import requests

from flask import render_template, render_template_string, jsonify, request

from app import app, db
from app.models import LocalNgrok


@app.route('/')
@app.route('/index')
def index():

    user = {'username': 'Bonanza'}

    return render_template('index.html', title='Home', user=user)


@app.route("/heatmap")
def heatmap_prototype():

    return render_template("heatmap.html")


@app.route('/proxy/<string:name>/<string:short_url>')
def proxy_to_local(name, short_url):

    local_ngrok_url = db.session.query(LocalNgrok.ngrok_url).filter(LocalNgrok.name == name).scalar()

    if local_ngrok_url is None:

        return render_template("index.html", title="Unable to find local ngrok by given name", user={"username": "Error"})

    # Forwarding user agent only
    headers = {"User-Agent": request.headers.get("user-agent")}

    response = requests.get(local_ngrok_url + "/api/" + short_url, headers=headers)

    return render_template_string(response.text)


@app.route('/proxy/<string:name>/api/<string:short_url>')
def proxy_to_local_api_in_path(name, short_url):

    local_ngrok_url = db.session.query(LocalNgrok.ngrok_url).filter(LocalNgrok.name == name).scalar()

    if local_ngrok_url is None:

        return render_template("index.html", title="Unable to find local ngrok by given name", user={"username": "Error"})

    # Forwarding user agent only
    headers = {"User-Agent": request.headers.get("user-agent")}

    response = requests.get(local_ngrok_url + "/api/" + short_url, headers=headers)

    return render_template_string(response.text)


@app.route('/api/proxy', methods=["POST"])
def add_local_proxy():

    error = 202

    try:

        input_data = request.json

        app_secret = os.environ.get("APP_SECRET")

        secret = input_data.get("secret")

        if not secret:

            print("Secret is empty (or None)")

            return jsonify({"error": 201}), 400

        if secret != app_secret:

            print("Secrets do not match")
            print(secret)

            return jsonify({"error": 201}), 400

        name = input_data.get("name")

        if not name:

            print("name is empty (or None)")

            return jsonify({"error": 201}), 400

        ngrok_url = input_data.get("ngrok_url")

        if not ngrok_url:

            print("ngrok_url is empty (or None)")

            return jsonify({"error": 201}), 400

        local_ngrok = db.session.query(LocalNgrok).filter(LocalNgrok.name == name).first()

        if local_ngrok is None:

            local_ngrok = LocalNgrok(name=name)

        local_ngrok.ngrok_url = ngrok_url

        db.session.add(local_ngrok)
        db.session.commit()

        return jsonify({"error": 200}), 200

    except Exception as e:

        print(e)

    return jsonify({"error": error}), 400
