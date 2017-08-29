import os
from mautic import MauticOauth2Client, Contacts
import json

filename = 'data/mautic_creds.json'

def read_token():
    """
    Example of function for getting stored token
    :return: token dict
    """
    with open(filename, 'r') as f:
        return json.loads(f.read())


def update_token(token):
    """
    Example of function for token update
    """
    with open(filename, 'w') as f:
    	f.write(json.dumps(token, indent=4))


mautic_client = MauticOauth2Client(base_url=os.environ["MAUTIC_HOST"],
                                    client_id=os.environ["MAUTIC_KEY"],
                                    client_secret=os.environ["MAUTIC_SECRET"],
                                    token=read_token(),
                                    token_updater=update_token)

contacts = Contacts(client=mautic_client)