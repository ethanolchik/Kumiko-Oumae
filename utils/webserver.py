from flask import Flask
from threading import Thread
import requests
app = Flask('')
@app.route('/')
def main():
    link = "https://www.worldometers.info/coronavirus/"
    f = requests.get(link)
    return f.text

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()