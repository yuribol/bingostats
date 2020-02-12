import os
import requests

from flask import render_template, make_response, render_template_string

from app import app


@app.route('/')
@app.route('/index')
def index():

    user = {'username': 'Bonanza'}

    return render_template('index.html', title='Home', user=user)


@app.route('/proxy/<str:short_url>')
def proxy_to_local(short_url):

    local_ngrok_url = os.environ.get('LOCAL_NGROK_URL')

    response = requests.get(local_ngrok_url + "/" + short_url)

    return render_template_string(response.text)
