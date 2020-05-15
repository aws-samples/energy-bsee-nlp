import json
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import sys

indexDoc = {
 "mappings" : {
  "properties" : {
   "EVENT_DATE" : {
    "type" : "date"
   },
   "SN_WAR" : {
    "type" : "keyword"
   },
   "API_WELL_NUMBER" : {
    "type" : "keyword"
   },
   "DEPTH" : {
    "type" : "long"
   },
   "LOCATION" : {
    "type" : "geo_point"
   },
   "DAILY_REMARK" : {
    "type" : "text"
   },
   "EVENT_TYPE" : {
    "type" : "text"
   },
   "EVENT_TEXT" : {
    "type" : "text"
   },
   "EVENT_SCORE" : {
    "type" : "text"
   }
  }
 },
"settings" : {
 "number_of_shards": 1,
 "number_of_replicas": 0
 }
}

# Creates an ES Index if one doesn't already exist
def createIndex(esClient):
    try:
        print("Creating Index")
        res = esClient.indices.exists('events1')
        if res is False:
            esClient.indices.create('events1', body=indexDoc)
            print ('Created')
        return 1
    except Exception as E:
            print(E)
            exit(4)

def indexDocElement(esClient,response):
    try:
        print("Indexing Document")
        snWar = response['SN_WAR']
        apiWellNumber = response['API_WELL_NUMBER']
        depth = float(response['DEPTH'])
        location = response['LOCATION']
        dailyRemark = response['DAILY_REMARK']
        retval = esClient.index(index='events1', body={
            'EVENT_DATE': response['EVENT_DATE'],
            'SN_WAR': snWar,
            'API_WELL_NUMBER': apiWellNumber,
            'DEPTH': depth,
            'LOCATION': location,
            'DAILY_REMARK': dailyRemark,
            'EVENT_TYPE': response['EVENT_TYPE'],
            'EVENT_TEXT': response['EVENT_TEXT'],
            'EVENT_SCORE': response['EVENT_SCORE']
        })
        print('Success: ',snWar)
    except Exception as E:
        print("Document not indexed")
        print("Error: ",E)


def main(): 
    
    with open('BSEEdata.txt') as json_file:
        data = json.load(json_file)
    print (len(data['data']))
    es_endpoint = sys.argv[1]
    region = sys.argv[2]
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    try:
        esClient = Elasticsearch(
            hosts=es_endpoint,
            port=443,
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection)
        print (esClient.info())
    except Exception as E:
        print("Unable to connect to {0}".format(es_endpoint))
        print(E)
        exit(3)
    createIndex(esClient)
    for item in data['data']:
        try:
            indexDocElement(esClient,item)
        except Exception as e:
            print(e)
            print('Error inserting into Elasticsearch. Please check Cloudwatch Logs.')
            raise e

main()