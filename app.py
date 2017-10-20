from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/', methods=['POST'])
# def search_request():
#     query = request.form['search_query']
#     return query

@app.route('/search', methods=['GET'])
def search():
    print(request.args.get('q'))
    query = {
        "query": {
            "query_string": {
                "query": request.args.get('q')
            }
        }
    }

    payload = json.dumps(query)
    print(payload)

    r = requests.post("http://localhost:9200/_search", data=payload)

    print(r.json())
    print(type(r.json()))
    return str(r.json())
