# Author: Dr. Ling Ma
# https://il.linkedin.com/in/cvlingma

# use eve + mongo instead of hosing on Google firebase, because the latter only supports pure nodejs app
# however the api needs ifcopenshell python anyway, in addition, eve is a advanced REST api framework

import os
# from eve.io.mongo import Validator
import requests
import json
import schema
from eve.methods.get import get_internal,getitem_internal
# from eve.methods.delete import deleteitem_internal
from eve.methods.post import post_internal
from eve.methods.patch import patch_internal
# from flask import abort
# from bson.objectid import ObjectId

from os.path import join, dirname
# import numpy as np
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from util_scanner import Scanner

from eve import Eve

from flask import send_from_directory
import numpy as np

app = Eve(__name__)

# host pcd files
@app.route('/file/<fid>')
def hello_world(fid):
    return send_from_directory('pcd', fid+'.pcd', as_attachment=True)

###########################################
# get all the features, the pairwise feature's value is reversed, this helps front end viewer to easily hide these objects 
# app.on_fetched_resource_entityList+=get_entity_list

def add_scan(items):
    for item in items:
        entities = get_internal('entity',**{'TrimbleVersionID': item['TrimbleVersionID']})[0]['_items']
        
        # get scanner view
        viewer={
            'x':item['CS_X'],
            'y':item['CS_Y'],
            'z':item['CS_Z'],
            'loc':item['CS_Origin']
        }
        l2g=np.array([viewer['x'],viewer['y'],viewer['z'],viewer['loc']]).transpose()
        l2g=np.concatenate((l2g,[[0,0,0,1]]),0)
        print(l2g)
        scanner=Scanner()
        points=scanner.scan(l2g,entities,item['Resolution'])
        scanner.savePCD(points,item['TrimbleVersionID'],str(item['_id']),l2g)
        
app.on_inserted_scanner+=add_scan

if __name__ == '__main__':
    # app.run()
    # particularly for cloud 9 use
    app.run(host=os.environ['IP'],port=int(os.environ['PORT']),debug=True)