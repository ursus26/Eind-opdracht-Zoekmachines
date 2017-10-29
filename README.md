Dependencies: pip install flask

How to run elasticsearch: ./elasticsearch-5.6.3/bin/elasticsearch -d
Windows: elasticsearch-5.6.3\bin\elasticsearch -d
How to run website: FLASK_APP=app.py FLASK_DEBUG=1 python -m flask run
Windows: python app.py

Upload data to elasticsearch: curl -XPOST localhost:9200/_bulk --data-binary @path/to/file
Deleta all data from elasticsearch: curl -XDELETE localhost:9200/_all
