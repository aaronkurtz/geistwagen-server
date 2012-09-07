import os,sys
import logging
sys.path.append(os.path.join(os.getenv("OPENSHIFT_REPO_DIR"), "libs"))
from pysoup import verify_bones_file

from bottle import route, get, post, request, default_app
from bottle import abort
import bson
import pymongo
import random
import md5


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
  count = mongo_db.bones.count()
  if 0 == count:
      abort(400, 'No bones exist\n')
  result = mongo_db.bones.find().limit(-1).skip(random.randrange(0,count)).next()
  return str(result['file'])
#TODO use Content Disposition to suggest filename
  

@post('/bones.<level>')
def upload():
  data = request.body.readline()
  if not data:
    abort(400, 'No data received\n')
  elif not (verify_bones_file(data)):
    abort(403, 'Bad data received\n')
  m = md5.new()
  m.update(data)
  md5sum = m.hexdigest()
  ip = request.headers['X-Forwarded-For']
  document = {'file':bson.Binary(data), 'ip':ip, 'md5':md5sum, 'level':level}
  mongo_db.bones.insert(document)
  return 'Uploaded bones file\n'


# This must be added in order to do correct path lookups for the views
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_GEAR_DIR'], 
    'runtime/repo/wsgi/views/')) 

application=default_app()
