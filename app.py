# Author: Dr. Ling Ma
# https://il.linkedin.com/in/cvlingma
from flask import Flask, send_from_directory
import os
from dotenv import load_dotenv
import numpy as np
from pymongo import MongoClient
from bson import ObjectId
from util_scanner import Scanner
dotenv_path = '.env'
load_dotenv(dotenv_path)
MONGO_HOST= os.environ.get('MONGO_HOST')
MONGO_PORT= os.environ.get('MONGO_PORT')
MONGO_USERNAME= os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD= os.environ.get('MONGO_PASSWORD')
MONGO_DBNAME= os.environ.get('MONGO_DBNAME')
client = MongoClient(MONGO_HOST,int(MONGO_PORT))
db = client[MONGO_DBNAME]
db.authenticate(MONGO_USERNAME, MONGO_PASSWORD, source=MONGO_DBNAME)
    
app = Flask(__name__)

@app.route('/scan/<scanner_id>')
def scan(scanner_id):
    scanner_data=db["scanner"].find_one({"_id":ObjectId(scanner_id)})
    TrimbleVersionID=scanner_data["TrimbleVersionID"]
    entities=db["entity"].find({"TrimbleVersionID":TrimbleVersionID})
    viewer={
        'x':scanner_data['CS_X'],
        'y':scanner_data['CS_Y'],
        'z':scanner_data['CS_Z'],
        'loc':scanner_data['CS_Origin']
    }
    l2g=np.array([viewer['x'],viewer['y'],viewer['z'],viewer['loc']]).transpose()
    l2g=np.concatenate((l2g,[[0,0,0,1]]),0)
    
    scanner=Scanner()
    points=scanner.scan(l2g,entities,scanner_data['Resolution'])
    scanner.savePCD(points,TrimbleVersionID,str(scanner_data['_id']),l2g)
    return "ready"
    
@app.route('/file/<fid>')
def download_pcd(fid):
    return send_from_directory('', fid+'.pcd', as_attachment=True)
    
if __name__ == '__main__':
    app.run(host=os.environ['IP'],port=int(os.environ['PORT']),debug=True)