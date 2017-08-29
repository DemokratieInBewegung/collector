
from flask import Flask, request

from cfg import PLZs, SPIKA
from mautic_client import contacts
from sync_to_gcontacts import push_to_gcontact

import os
import logging

app = Flask(__name__)


@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.WARN)


@app.route('/plz-fix/{}'.format(os.environ['INCOMING_KEY']), methods=["POST"])
def fixing_plz():
	data =  request.get_json(force=True)
	try:
		payload = data["mautic.lead_post_save_new"]
	except KeyError:
		payload = data["mautic.lead_post_save_update"]

	for entry in payload:
		fields = entry["contact"]['fields']
		state = fields['core'].get("state", {}).get("value", None)
		plz = fields['core'].get("zipcode", {}).get("value", None).strip()
		if len(plz) == 4:
			plz = "0{}".format(plz)
		butawa17_spika = (fields['personal'] or {}).get("butawa17_spika", {}).get("value", None)

		if butawa17_spika: continue  # we are already done here
		if not plz: continue         # nothing we can do here

		to_update = {
			'butawa17_spika': SPIKA.get(plz, '')
		}

		if not state:
			to_update['state'] = PLZs.get(plz, '')

		resp = contacts.edit(entry['contact']['id'], to_update)

		if 'errors' in resp:
			app.logger.warning("Fixing PLZ failed: {errors}".format(**resp))
			app.logger.warning("--" * 20)


	return "ok"


@app.route('/gcontacts-sync/{}'.format(os.environ['INCOMING_KEY']), methods=["POST"])
def send_to_gcontacts():
	payload = request.get_json(force=True)["mautic.lead_post_save_update"]
	for entry in payload:
		if 'butawa17-spika-synced' in entry['contact']['tags']: continue # we are already done here

		fields = entry["contact"]['fields']
		butawa17_spika = (fields["personal"] or {}).get("butawa17_spika", {}).get("value", None)
		whatsapp = (fields["social"] or {}).get("whatsapp", {}).get("value", None)

		if not butawa17_spika: continue  # nothing we can do here
		if not whatsapp: continue  # nothing we can do here

		res = push_to_gcontact(butawa17_spika, {
			"phoneNumbers": [{"value": whatsapp}],
			"names": [{
				"familyName": fields.get("lastname", {}).get("value", ""),
				"givenName": fields.get("firstname", {}).get("value", "")
				}]
			})

		tags = entry['leads']['tags'] + ['butawa17-spika-synced']
		if "error" in res:
			tags.append('butawa17-spika-sync-failed')
			app.logger.warning("Sync Failed: {error}".format(**res))
			app.logger.warning(entry)
			app.logger.warning("--" * 20)

		contacts.edit(entry['lead']['id'], {
			"tags": ",".join(tags)
		})

	return "ok"