import os, redis
from flask import Flask
app = Flask(__name__)
r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)
@app.route("/")
def index():
    return f"Visites : {r.incr('visites')}\n"
