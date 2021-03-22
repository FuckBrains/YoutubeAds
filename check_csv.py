import csv
from pprint import pprint

filename = 'youtube_ads_test_12.csv'
infile = open(filename, newline = '', encoding = 'utf-8')
reader = csv.DictReader(infile)

count = 0
ad_count = 0
removed = 0
ad_types = {'banner':0, 'preroll':0}
advertisers = {}
targeting = {}
offsite = {'paypal' : 0, 'patreon' : 0, 'twitter': 0, 'parler' : 0, 'sponsor' : 0, 'gofundme' : 0, 'facebook': 0, 'rumble' : 0, ' gab ' : 0, 'gab:' : 0, 'telegram' : 0}

seen = {}

for row in reader:
	if row['videoid'] in seen:
		continue
	else:
		seen[row['videoid']] = 1

	count += 1
	if row['advertiser']: 
		ad_count += 1
		ad_types[row['ad_type']] += 1

		advertiser = row['advertiser']
		if advertiser in advertisers:
			advertisers[advertiser] += 1
		else:
			advertisers[advertiser] = 1

		for reason in row['targetinginfo'].strip("[]").split(','):
			if reason in targeting:
				targeting[reason] +=1
			else:
				targeting[reason] = 1

	description = row['descr']
	for site in offsite.keys():
		if site in description:
			offsite[site] += 1

	if row['removed'] == 'True':
		removed += 1



print(count, " videos")
print(ad_count, " ads seen")
print(removed, " removed")

pprint(ad_types)
pprint(advertisers)
pprint(targeting)
pprint(offsite)