import logging

from flask import Flask, render_template, request
from google.appengine.ext import ndb
from google.appengine.api import memcache


application = Flask(__name__)

class Version(ndb.Model):
   likes=ndb.FloatProperty()
   views=ndb.FloatProperty()

v1=Version.get_by_id('v1')
if not v1:
   v1=Version(likes=1,views=1,id='v1')
   v1_key=v1.put()

v2=Version.get_by_id('v2')
if not v2:
   v2=Version(likes=1,views=1,id='v2')
   v2_key=v2.put()

@application.route('/')
def home():
   v1_last=Version.get_by_id('v1')
   v1_last.views+=1
   v1_last.put()
   return render_template('home.html')

@application.route('/sumav1', methods=['POST'])
def sumav1():
   v1_last=Version.get_by_id('v1')
   v1_last.likes+=1
   v1_last.put()
   return render_template('like-v1.html')

@application.route('/dashboard')
def dashboard():
    vistas1=Version.get_by_id('v1').views
    vistas2=Version.get_by_id('v2').views
    likes1=Version.get_by_id('v1').likes
    likes2=Version.get_by_id('v2').likes
    return render_template('dashboard.html',v=[round(likes1/vistas1,3),round(likes2/vistas2,3),vistas1,likes1,vistas2,likes2])

@application.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]

