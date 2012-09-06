import os,sys
sys.path.append(os.path.join(os.getenv("OPENSHIFT_REPO_DIR"), "libs"))
from pysoup import verify_bones_file

from bottle import route, get, put, request, default_app
from bottle import abort
import pymongo
import random


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
  count = mongo_db.bones.count()
  if 0==count:
      abort(400, 'No bones exist')
  result = mongo_db.bones.find().limit(-1).skip(random.randrange(0,count)).next()
  return result
  

@put('/bones')
def upload():
  data = request.body.readline()
  if not data:
    abort(400, 'No data received')
  elif not (verify_bones_file):
    abort(400, 'Bad data received')
  mongo_db.bones.insert(data)
  return 'Uploaded bones file'


# This must be added in order to do correct path lookups for the views
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_GEAR_DIR'], 
    'runtime/repo/wsgi/views/')) 

application=default_app()
