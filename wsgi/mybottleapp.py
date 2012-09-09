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
#TODO ban abusive downloaders
  ip = request.headers['X-Forwarded-For']
#TODO exclude already existing levels to avoid overwriting ghosts through query
  debug = request.query.debug or False
  sameip = request.query.sameip or False
  exclude = request.query.exlude or False
  if sameip:
    count = mongo_db.bones.count()
    if 0 == count:
      abort(404, 'No bones exist\n')
    result = mongo_db.bones.find().limit(-1).skip(random.randrange(0,count)).next()
  else:    
    cursor = mongo.db_bones.find({'ip':{'$nin':[ip]}})
    count = cursor.count()
    if 0 == count:
      abort(404, 'No bones exist\n')
    result = cursor.limit(-1).skip(random.randrange(0,count)).next()
  response.set_header('Content-Disposition','attachment; filename=bones.'+result['level'])
  if debug:
      return request.query.items() + request.query_string + result['level'] + "Count: " + count
  return str(result['file'])
  

@post('/bones.<level>')
def upload(level):
  #TODO blacklist trolls
  if request.content_length > (100*20):
    abort(403, 'Bad data received\n')
  data = request.body.read()
  if not data:
    abort(400, 'No data received\n')
  elif not (verify_bones_file(data)):
    abort(403, 'Bad data received\n')
  md5sum = hashlib.md5(data).hexdigest()
  if mongo_db.bones.find({'md5':md5sum}).count():
    abort(401, 'File already exists\n')
  ip = request.headers['X-Forwarded-For']
  document = {'file':bson.Binary(data), 'ip':ip, 'md5':md5sum, 'level':level}
  mongo_db.bones.insert(document)
  return 'Uploaded bones file\n'


# This must be added in order to do correct path lookups for the views
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_GEAR_DIR'], 
    'runtime/repo/wsgi/views/')) 

application=default_app()
