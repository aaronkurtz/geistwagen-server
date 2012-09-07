import os,sys
import logging
sys.path.append(os.path.join(os.getenv("OPENSHIFT_REPO_DIR"), "libs"))
from pysoup import verify_bones_file

from bottle import route, get, post, request, response, abort
from bottle import default_app
import bson
import pymongo
import random
import hashlib


mongo_con = pymongo.Connection(
  os.environ['OPENSHIFT_NOSQL_DB_HOST'],
  int(os.environ['OPENSHIFT_NOSQL_DB_PORT']))

mongo_db = mongo_con[os.environ['OPENSHIFT_APP_NAME']]
mongo_db.authenticate(os.environ['OPENSHIFT_NOSQL_DB_USERNAME'],
                      os.environ['OPENSHIFT_NOSQL_DB_PASSWORD'])

@route('/')
def index():
    return 'Geistwagen'

@get('/bones')
def download():
  ip = request.headers['X-Forwarded-For']
#TODO only download files uploaded from other IPs
  count = mongo_db.bones.count()
  if 0 == count:
      abort(400, 'No bones exist\n')
  result = mongo_db.bones.find().limit(-1).skip(random.randrange(0,count)).next()
  response.set_header('Content-Disposition','filename=bones.'+result['level'])
  return str(result['file'])
  

@post('/bones.<level>')
def upload(level):
  if request.content_length > (100*20):
    abort(400, 'Improper data received\n')
  data = request.body.read()
  if not data:
    abort(400, 'No data received\n')
  elif not (verify_bones_file(data)):
    abort(403, 'Bad data received\n')
  md5sum = hashlib.md5(data).hexdigest()
  #TODO check if file was already uploaded
  ip = request.headers['X-Forwarded-For']
  document = {'file':bson.Binary(data), 'ip':ip, 'md5':md5sum, 'level':level}
  mongo_db.bones.insert(document)
  return 'Uploaded bones file\n'


# This must be added in order to do correct path lookups for the views
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_GEAR_DIR'], 
    'runtime/repo/wsgi/views/')) 

application=default_app()
