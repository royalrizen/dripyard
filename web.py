from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Good job! Now copy the url and create a cron-job."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
