import csv
from pprint import pprint
import os

filenames = os.listdir('tests/')
print(filenames)


fieldnames = open('tests/' + filenames[0],'r', errors='ignore').readline().strip().split(',')


channel_links = {}
channel_offsite = {}
channel_advertisers = {}
ad_types = {'banner':{}, 'preroll':{}}
advertisers = {}


offsite = {'paypal' : 0, 'patreon' : 0, 'twitter': 0, 'parler' : 0, 'sponsor' : 0, 'gofundme' : 0, 'facebook': 0, 'rumble' : 0, ' gab ' : 0, 'gab:' : 0, 'telegram' : 0, 'donation' : 0, 'bitchute' : 0, 'merch': 0, 'merchandise': 0, 'steemit' : 0}
offsite_no_ads = {'paypal' : 0, 'patreon' : 0, 'twitter': 0, 'parler' : 0, 'sponsor' : 0, 'gofundme' : 0, 'facebook': 0, 'rumble' : 0, ' gab ' : 0, 'gab:' : 0, 'telegram' : 0, 'donation' : 0}
offsite_vids = {}

# for filename in filenames:


for filename in filenames:

	infile = open("tests/" + filename, newline = '', encoding = 'utf-8')
	reader = csv.DictReader(infile)

	for row in reader:
		channel_id = row['channelid']

		if row['advertiser']:
			if channel_id in channel_advertisers:
				pass
			else:
				channel_advertisers[channel_id] = {}

			ad_type = row['adtype']
			adurl = row['advertiser']

			if adurl in ad_types[ad_type]:
				ad_types[ad_type][adurl] += 1
			else:
				ad_types[ad_type][adurl] = 1

			if adurl in advertisers:
				advertisers[adurl] += 1
			else:
				advertisers[adurl] = 1

			if adurl in channel_advertisers[channel_id]:
				channel_advertisers[channel_id][adurl] += 1
			else:
				channel_advertisers[channel_id][adurl] = 1

		if channel_id in channel_offsite:
			pass
		else:
			channel_offsite[channel_id] = {}
			channel_links[channel_id] = {}

		for link in row['descrurls'].split('&&&&'):
			offsite_flag = False
			for key in offsite:
				if key in link:
					offsite_flag = True
					break

			if offsite_flag:
				if link in channel_offsite[channel_id]:
					channel_offsite[channel_id][link] += 1
				else:
					channel_offsite[channel_id][link] = 1

			else:
				if link in channel_links[channel_id]:
					channel_links[channel_id][link] += 1
				else:
					channel_links[channel_id][link] = 1		
					

outfile = open('advertisers.csv', 'w')
fieldnames = ['advertiser', 'count']
writer = csv.DictWriter(outfile, fieldnames)
writer.writeheader()

for advertiser in advertisers:
	towrite = {'advertiser':advertiser, 'count' : advertisers[advertiser]}
	writer.writerow(towrite)

outfile.close()


outfile = open('ads_by_channel.csv', 'w')
fieldnames = ['channel', 'advertiser', 'count']
writer = csv.DictWriter(outfile, fieldnames)
writer.writeheader()

for channel in channel_advertisers:
	for advertiser in channel_advertisers[channel]:
		towrite = {'channel' : channel, 'advertiser':advertiser, 'count' : channel_advertisers[channel][advertiser]}
		writer.writerow(towrite)

outfile.close()


outfile = open('ads_by_type.csv', 'w')
fieldnames = ['adtype', 'advertiser', 'count']
writer = csv.DictWriter(outfile, fieldnames)
writer.writeheader()

for ad_type in ad_types:
	for advertiser in ad_types[ad_type]:
		towrite = {'adtype' : ad_type, 'advertiser':advertiser, 'count' : ad_types[ad_type][advertiser]}
		writer.writerow(towrite)

outfile.close()


outfile = open('offsite_by_channel.csv', 'w')
fieldnames = ['channel', 'offsite_link', 'count']
writer = csv.DictWriter(outfile, fieldnames)
writer.writeheader()

for channel in channel_offsite:
	for link in channel_offsite[channel]:
		towrite = {'channel' : channel, 'offsite_link':link, 'count' : channel_offsite[channel][link]}
		writer.writerow(towrite)

outfile.close()


outfile = open('links_by_channel.csv', 'w')
fieldnames = ['channel', 'link', 'count']
writer = csv.DictWriter(outfile, fieldnames)
writer.writeheader()

for channel in channel_links:
	for link in channel_links[channel]:
		towrite = {'channel' : channel, 'link':link, 'count' : channel_links[channel][link]}
		writer.writerow(towrite)

outfile.close()