import httplib2
import json

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets

import os
import json
import couchdb
import requests
import logging
logging.basicConfig(level=logging.DEBUG)


def push_to_gcontact(entry, payload):

	storage = Storage('data/{}.dat'.format(entry))
	flow = flow_from_clientsecrets('data/gclient_secrets.json',
	                               scope='https://www.googleapis.com/auth/contacts',
	                               redirect_uri='http://example.com/auth_return')

	credentials = storage.get()
	# Create an httplib2.Http object to handle our HTTP requests and
	# authorize it with our good Credentials.
	http = httplib2.Http()
	http = credentials.authorize(http)

	(resp, content) = http.request("https://people.googleapis.com/v1/people:createContact", "POST",
		body=json.dumps(paylod))

	if resp['status'] != '200':
		return {
			"error": resp,
			"content": content
		}

	else:
		{
			"synced_to": entry,
			"gcontacts_id": json.loads(content.decode('utf-8'))['resourceName']
		}
