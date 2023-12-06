###############################################################
## This function is to populate a dynamoDB table with a CSV ###
###############################################################

import json
import csv
import boto3
import os
import time

BASE_PATH = '/tmp/'
CSV_SEPARATOR = ';'

ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['TABLE_NAME'])
s3_client = boto3.client('s3')

def save_item_ddb(table,item):
    response = table.put_item(Item=item)
    return response
    
def descarga_archivo(bucket, key, base_path, filename):
    with open(base_path+filename, "wb") as data:
        s3_client.download_fileobj(bucket, key, data)
    return True


def lambda_handler(event, contex):
    print(event)
    print('Se han encontrado {} archivo(s) en el bucket nuevo(s)'.format(len(event['Records'])))
 
    for record in event['Records']:
        bucket1 = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        filename = key.split('/')[-1]
        descarga_archivo(bucket1, key, BASE_PATH, filename)
        jsonFilePath = BASE_PATH+filename
        print('Empieza la lectura de {}'.format(jsonFilePath)) 

        with open(jsonFilePath) as json_file:
            data = json.load(json_file)

        for row in data:
            save_item_ddb(table,row)

    
