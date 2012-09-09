import os,sys
import logging
import datetime
sys.path.append(os.path.join(os.getenv("OPENSHIFT_REPO_DIR"), "libs"))
from pysoup import verify_bones_file

from bottle import route, get, put, request, response, abort
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
#TODO ban abusive downloaders
  debug = request.query.debug or False
  keep = request.query.exclude or False
  if request.query.sameip:
      blockip = []
  else:
      blockip = ip
  excluded = request.query.exclude.split('.') or []
  cursor = mongo_db.bones.find({'ip':{'$nin':[blockip]},'level':{'$nin':excluded}})
  count = cursor.count()
  if 0 == count:
    if debug:
      return str((request.query_string , keep, ip, excluded, count))
    abort(404, 'No bones exist\n')
  result = cursor.limit(-1).skip(random.randrange(0,count)).next()
  if debug:
      return str((request.query_string , keep, ip, excluded, count, result['level']))
  response.set_header('Content-Disposition','attachment; filename=bones.'+result['level'])
  if not keep:
      mongo_db.bones.remove({'_id':result['id']})
      result['downloader'] = ip
      result['downloaded date'] = datetime.datetime.utcnow()
      mongo_db.old_bones.insert(result)
  return str(result['file'])
  

@put('/bones.<level>')
def upload(level):
  ip = request.headers['X-Forwarded-For']
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
  document = {'file':bson.Binary(data), 'ip':ip, 'md5':md5sum, 'level':level, 'date':datetime.datetime.utcnow()}
  mongo_db.bones.insert(document)
  return 'Uploaded bones file\n'


# This must be added in order to do correct path lookups for the views
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_GEAR_DIR'], 
    'runtime/repo/wsgi/views/')) 

application=default_app()
