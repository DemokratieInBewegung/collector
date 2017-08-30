
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
		fields = entry["contact"]['fields']
		personal = (fields["personal"] or {})
		core = (fields["core"] or {})

		if personal.get("butawa17_spika_synced", {}).get("value", None) == 'synced': continue
		
		butawa17_spika = (fields["personal"] or {}).get("butawa17_spika", {}).get("value", None)
		whatsapp = (fields["social"] or {}).get("whatsapp", {}).get("value", None)

		if not butawa17_spika: continue  # nothing we can do here
		if not whatsapp: continue  # nothing we can do here

		error = False

		try:
			res = push_to_gcontact(butawa17_spika, {
				"phoneNumbers": [{"value": whatsapp}],
				"names": [{
					"familyName": core.get("lastname", {}).get("value", ""),
					"givenName": core.get("firstname", {}).get("value", "")
					}]
				})
		except Exception as e:
			tags.append('butawa17-spika-sync-failed')
			app.logger.warning("Sync Failed:")
			app.logger.error(e)
			error = True
		else:
			if "error" in res:
				efror = True
				app.logger.warning("Sync Failed: {error}".format(**res))
				app.logger.warning(entry)
				app.logger.warning("--" * 20)

		contacts.edit(entry['lead']['id'], {
			"butawa17_spika_synced": "failed" if error else "synced"
		})

	return "ok"