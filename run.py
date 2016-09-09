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
app = Eve()


###########################################
# get all the features, the pairwise feature's value is reversed, this helps front end viewer to easily hide these objects 
# app.on_fetched_resource_entityList+=get_entity_list

if __name__ == '__main__':
    # app.run()
    # particularly for cloud 9 use
    app.run(host=os.environ['IP'],port=int(os.environ['PORT']),debug=True)