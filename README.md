### Studenten
Marit Beerepoot - 10983430 <br>
Jessy Bosman - 11056045 <br>
Vincent Damen - 11034734 <br>
Bart de Haan - 11044616 <br>

### Answers to the questions
https://github.com/ursus26/Eind-opdracht-Zoekmachines/wiki

### Dependencies
pip install flask <br>
pip install ntlk
Also install nltk stopwords dutch
elasticsearch 5.6.3

### Data
Our data files we used: https://drive.google.com/drive/folders/0B7LqDuzfzVmqb3l1b3ZFRlNFSEk?usp=sharing

### How to run
###### How to run elasticsearch
Linux & macOS: ./elasticsearch-5.6.3/bin/elasticsearch -d <br>
Windows: elasticsearch-5.6.3\bin\elasticsearch -d <br>

###### Sending data to elasticsearch
Upload data to elasticsearch: python send_data_to_elasticsearch.py ./path/to/data/folder <br>
Deleta all data from elasticsearch: curl -XDELETE localhost:9200/_all

###### How to run server
python app.py
