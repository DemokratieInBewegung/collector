import csv

with open('plz_zu_state.csv', 'r') as inp:
	PLZs = {row[0]: row[1] for row in csv.reader(inp)}

with open('plz_zu_spika.csv', 'r') as inp:
	SPIKA = {row[0]: row[1] for row in csv.reader(inp)}
