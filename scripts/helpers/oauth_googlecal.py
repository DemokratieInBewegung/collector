import argparse
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client import tools

parser = argparse.ArgumentParser(parents=[tools.argparser])
flags = parser.parse_args()

storage = Storage('info.dat')
flow = flow_from_clientsecrets('gclient_secrets.json',
                               scope='https://www.googleapis.com/auth/contacts',
                               redirect_uri='http://example.com/auth_return')

flow.params['access_type'] = 'offline'         # offline access
credentials = tools.run_flow(flow, storage, flags)