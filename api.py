#import json,os
import logging
#import sys
#import requests
from flask import Flask, request, Response, jsonify
#from flask_restful import Api, Resource, reqparse
#import flasgger
#from flasgger import Swagger, swag_from
import pickledb

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
 level=logging.INFO
)

logger = logging.getLogger(__name__)

#db = pickledb.load("bot.db", False)
#if not db.get("text"):
#    db.set("text", "test")

app = Flask(__name__)

db = pickledb.load("bot.db", False)

#template = {
#  "swagger": "2.0",
#  "info": {
#    "title": "My API",
#    "description": "API for my data",
#    "contact": {
#      "responsibleOrganization": "ME",
#      "responsibleDeveloper": "Me",
#      "email": "me@me.com",
#      "url": "www.me.com",
#    },
#    "termsOfService": "http://me.com/terms",
#    "version": "0.0.1"
#  },
#  "host": "162.0.225.132:5000", # overrides localhost:500
#  "basePath": "/api", # base bash for blueprint registration
#  "schemes": [
#    "http",
#    "https"
#  ],
#  "operationId": "getmyData"
#}
#swagger = Swagger(app, template=template)

#print(template)

#@app.route('/bot_text/',methods = ['GET'])
@app.route('/test/')
def get_bot_text():
#    global db
#    db = pickledb.load("bot.db", False)
#    main()
    text = db.get("text")
    print(text, "****+++++x")
#    return jsonify({"class_name":text})
    return text

def main():
#    print("change database*******")
#    global db
#    db = pickledb.load("bot.db", False)
#    print("database changed*****")
    pass

if __name__ == "__main__":
    main()
    app.run(debug=True, host = '162.0.225.132')
#    socketio.run(app, debug=True, host = '162.0.225.132')

