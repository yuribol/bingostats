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


@app.route('/proxy/<string:short_url>')
def proxy_to_local(short_url):

    local_ngrok_url = os.environ.get('LOCAL_NGROK_URL')

    response = requests.get(local_ngrok_url + "/" + short_url)

    return render_template_string(response.text)


@app.route('/api/proxy')
def add_local_proxy():

    error = 202

    try:

        input_data = request.json()

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