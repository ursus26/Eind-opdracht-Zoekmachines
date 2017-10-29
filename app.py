from flask import Flask, render_template, request, jsonify
import requests
import json
import sys
import collections

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():

    print(request.args.get('optradio'))

    # Create a query
# Set the fields we search in.
    fields = []
    if request.args.get('optradio'):
        if request.args.get('optradio') == "title":
            fields.append("question")
        else:
            fields.append("description")

    else:
        fields.append("description")
        fields.append("title")

    # Create a query
    query = {
        "query": {
            "multi_match": {
                "query": request.args.get('q'),
                "fields": fields
            }
        }
    }

    # Send a search request to elasticsearch and get a response
    payload = json.dumps(query)
    r = requests.post("http://localhost:9200/_search", data=payload)

    # create list of dicts with all information of a question
    queryQuestions = []
    print(r.json())
    for listitem in r.json()[u'hits']['hits']:
        queryQuestions.append(listitem)

    time_x, time_y = timeline(r.json())
    return render_template('search.html', queryQuestions=queryQuestions, query=request.args.get('q'), time_x=json.dumps(time_x), time_y=time_y)


@app.route('/view_question', methods=['GET'])
def view_question():
    query = {
        "query": {
            "query_string": {
                "query": request.args.get('q'),
                "fields": ["questionId"]
            }
        }
    }

    # Send a search request to elasticsearch and get a response
    payload = json.dumps(query)
    r_answers = requests.post("http://localhost:9200/goedevragen/answers/_search", data=payload)
    r_question = requests.post("http://localhost:9200/goedevragen/questions/_search", data=payload)

    question_answers = []
    for listitem in r_answers.json()[u'hits']['hits']:
        question_answers.append(listitem)


    wordcloudList = []
    question = r_question.json()[u'hits']['hits'][0]
    for x in question_answers:
        for y in x[u'_source'][u'answer'].split(' '):
            wordcloudList.append(y)
    wordcloud = collections.Counter(wordcloudList)
    wordcloudIndex = sorted(wordcloud.items(), key=lambda x: x[1])

    return render_template('view_question.html', question=question, question_answers=question_answers, wordcloud=wordcloudIndex)

def timeline(query_result):
    """
    Creates a timeline of the query result based on the years.
    """
    hits = query_result[u'hits']['hits']
    year_count = {}

    # Get the number of questions for each year.
    for hit in hits:
        if hit['_source']['date'][:4] not in year_count:
            year_count[hit['_source']['date'][:4]] = 1

        year_count[hit['_source']['date'][:4]] += 1

    years = sorted(year_count.keys(), key=lambda x:x.lower())
    x = []
    y = []
    sum_count = 0
    for year in years:
            x.append(int(year))
            y.append(int(year_count[year]))


    print((x, y))
    return x, y

if __name__ == '__main__':
    app.run(debug=True)
