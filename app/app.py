from bson import json_util, ObjectId
from flask import Flask
from flask import request

from app.helpers import mongo_client

import dateutil.parser

API_VERSION = '1.0'

app = Flask(__name__)
db = mongo_client()


@app.route('/')
def root():
    response = {'apiVersion': API_VERSION, 'appName': 'Topbox Backend Take Home Test'}
    return json_util.dumps(response)


@app.route('/clients')
def clients():
    return json_util.dumps(db.clients.find({}))


@app.route('/clients/<client_id>')
def clients_by_id(client_id):
    client_object_id = ObjectId(client_id)
    return json_util.dumps(db.clients.find_one({'_id': client_object_id}))


@app.route('/engagements')
def engagements():
    return json_util.dumps(db.engagements.find({}))


@app.route('/engagements/<engagement_id>')
def engagements_by_id(engagement_id):
    engagement_object_id = ObjectId(engagement_id)
    return json_util.dumps(db.engagements.find_one({'_id': engagement_object_id}))


@app.route('/interactions')
def interactions():
@app.route('/interactions')
def interactions():
	queryParams = request.args
	engagementId = queryParams.get('engagementId')
	response = None
	if engagementId is None:
		response = {'error': 'Mandatory parameter engagementId is missing'}
	elif not ObjectId.is_valid(engagementId):
		response = {'error': 'Value of mandatory parameter engagementId is not valid'}
	else:
		dbFilterParams = {'engagementId': ObjectId(engagementId)}
		interactionDate = queryParams.get('interactionDate')
		if interactionDate is not None:
			try:
				dbFilterParams['interactionDate'] = dateutil.parser.parse(interactionDate)
			except:
				print("InteractionData is not a valid date.. Ignoring the parameter")
		response = db.interactions.find(dbFilterParams)
	return json_util.dumps(response)


@app.route('/interactions/<interaction_id>')
def interactions_by_id(interaction_id):
    interaction_object_id = ObjectId(interaction_id)
    return json_util.dumps(db.interactions.find_one({'_id': interaction_object_id}))
