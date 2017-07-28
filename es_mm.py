# -*- coding: utf-8 -*-

import requests
import json

def search(uri, term):
    query = json.dumps({
        "from": 0,
        "size": 1000,

        "query": {
            "multi_match": {
                "query": term,
                "fields": [
                    "CHNL_NM^3",
                    "artist_nm",
                    "track_nm"
                ]
            }
        }
    })
    response = requests.get(uri, data=query)
    results = json.loads(response.text)
    return results



def keyword_anal(uri, term):
    query = json.dumps({
        "analyzer": "korean",
        "text": term
    })
    response = requests.get(uri, data=query)
    results = json.loads(response.text)
    return results




def format_results(results):
    data = [doc for doc in results['hits']['hits']]
    for doc in data:
        print("Playlist:%-40s   ArtistName:%-30s    TrackName:%-30s") % (doc['_source']['CHNL_NM'],doc['_source']['artist_nm'],doc['_source']['track_nm'])


def format_anal_results(results):
    data = [doc for doc in results['tokens']]
    for doc in data:
        print("token:%-20s") % (doc['token'])


while True:
    keyword = raw_input("enter search keywords:")
    keyworld_anal_result = keyword_anal("http://localhost:9200/mm3/_analyze",keyword)
    result = search("http://localhost:9200/mm3/chnl3/_search",keyword)
    print("##검색 결과:")
    print(format_results(result))
    print("##질의어 분석 결과:")
    print(format_anal_results(keyworld_anal_result))
