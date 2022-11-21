import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
import json
from psycopg2 import connect
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
dir = os.path.dirname(__file__)
with open(os.path.join(dir, 'db_credentials')) as data:
    db_credentials = json.load(data)
@app.route("/")
def index():
    conn = connect(
        dbname='postgres',
        user=db_credentials['username'],
        host=db_credentials['host'],
        password=db_credentials['password']
    )
    conn.close()
    return """
        <style>body {background-color: green}</style>
        <h1 style='color:black'>Everything is working fine</h1>
    """
@app.route("/error/")
def error():
    conn = connect(
        dbname='postgres',
        user=db_credentials['username'],
        host=db_credentials['host'],
        password='asdf1234'
    )
    return "error"

    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)