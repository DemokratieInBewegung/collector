import os
import json
import couchdb
import requests
import csv
import logging
logging.basicConfig(level=logging.DEBUG)
from cfg import PLZs, SPIKA

from mautic_client import contacts


couch = couchdb.Server(os.environ["COUCHDB_URL"])['cllctr']


def import_to_mautic(limit=10):

	for doc in couch.view('to_import_to_mautic/to_import_to_mautic', options={"limit": limit}):
		doc = couch[doc.id]

		if 'synced_to_mautic' in doc:
			# reached a scenario in which we both started updating. end here
			break


		#  clean up
		contact = dict(doc)

		contact.pop("_rev")
		contact.pop("age", False)
		contact.pop("type", False)

		try:
			contact["agegroup"] = contact.pop("agegroup", {}).get("value", None)
		except AttributeError:
			pass
		contact["whatsapp"] = contact.get("mobile", '')
		contact['points'] = 5

		contact["id"] = contact.pop("_id")
		zipcode = str(contact.get('zipcode', PLZs.get('plz', ''))).strip()
		contact["state"] = PLZs.get(zipcode, '')
		contact['butawa17_spika'] = SPIKA.get(zipcode, '')
		tags = ["swk-butawa-17"]

		for x in ('pot-member', 'pot-bewegerin', 'pot-volunteer', 'newsletter'):
			if contact.pop(x, False):
				tags.append(x)

		contact["tags"] = ",".join(tags)
		try:
			resp = contacts.create(contact)
		except Exception as e:
			doc['synced_to_mautic'] = {
				"error": "{}".format(e)
			}
			print("Error Adding: {firstname} {lastname} <{email}>, {mobile}".format(**contact))
			print(e)
		else:
			doc['synced_to_mautic'] = {
				"mautic_id": resp["contact"]["id"],
				"added": resp["contact"]["dateAdded"]
			}
			print("Added #{}: {firstname} {lastname} <{email}>, {mobile}".format(resp["contact"]["id"], **contact))
		couch.save(doc)


if __name__ == '__main__':
	import_to_mautic(limit=1)