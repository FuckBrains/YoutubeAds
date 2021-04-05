import csv
from pprint import pprint
import os

filenames = os.listdir('tests/')

count = 0
ad_count = 0
removed = 0

unique_count = 0
channel_count = 0
channels_seen = {}
channel_ads = {}
channel_advertisers = {}
video_ads = {}
adtypes = {'banner':0, 'preroll':0}
advertisers = {}
seen = {}


targeting = {}
offsite = {'paypal' : 0, 'patreon' : 0, 'twitter': 0, 'parler' : 0, 'sponsor' : 0, 'gofundme' : 0, 'facebook': 0, 'rumble' : 0, ' gab ' : 0, 'gab:' : 0, 'telegram' : 0, 'donation' : 0}
offsite_no_ads = {'paypal' : 0, 'patreon' : 0, 'twitter': 0, 'parler' : 0, 'sponsor' : 0, 'gofundme' : 0, 'facebook': 0, 'rumble' : 0, ' gab ' : 0, 'gab:' : 0, 'telegram' : 0, 'donation' : 0}
offsite_vids = {}

for filename in filenames:

	infile = open("tests/" + filename, newline = '', encoding = 'utf-8')
	reader = csv.DictReader(infile)

	for row in reader:
		video_id = row['videoid']
		if video_id in seen:
			seen[video_id] += 1
		else:
			unique_count += 1
			seen[video_id] = 1

		channel_id = row['channelid']
		if channel_id in channels_seen:
			channels_seen[channel_id] += 1
		else:
			channel_count += 1
			channels_seen[channel_id] = 1

		count += 1
		if row['advertiser']: 
			if channel_id in channel_ads:
				channel_ads[channel_id] += 1
			else:
				channel_ads[channel_id] = 1

			if video_id in video_ads:
				video_ads[video_id] += 1
			else:
				video_ads[video_id] = 1

			ad_count += 1
			adtypes[row['adtype']] += 1

			advertiser = row['advertiser']

			if advertiser in advertisers:
				if video_id in advertisers[advertiser]:
					advertisers[advertiser][video_id] += 1
				else:
					advertisers[advertiser][video_id] = 1
				
			else:
				advertisers[advertiser] = {video_id : 1}

			if advertiser in channel_advertisers:
				if advertiser in channel_advertisers[channel_id]:
					channel_advertisers[channel_id][advertiser] += 1
				else:
					channel_advertisers[channel_id][advertiser] = 1
				
			else:
				channel_advertisers[channel_id] = {advertiser : 1}


			for reason in row['targetinginfo']:
				if reason in targeting:
					targeting[reason] +=1
				else:
					targeting[reason] = 1

		description = row['descr']
		if seen[video_id] == 1:
			for site in offsite.keys():
				if site in description:
					offsite[site] += 1
					if video_id not in video_ads:
						offsite_no_ads[site] += 1

		if row['removed'] == 'True':
			removed += 1

	infile.close





pprint(adtypes)
print()
pprint(advertisers)
print()
pprint(targeting)
print()
pprint('offsite mentions')
pprint(offsite)
print()
pprint('offsite mentions on videos without ads')
pprint(offsite_no_ads)
print()
for channel in channel_ads:
	print(channel, 'seen', channels_seen[channel], "times with", channel_ads[channel], 'ads.')
	if (channel_ads[channel] > 0) and (channels_seen[channel] / channel_ads[channel] > 50):
		pprint(channel_advertisers[channel])

print(count, " videos")
print(unique_count, ' unique videos')
print(len(video_ads), " videos with ads")
print(ad_count, " ads seen")
print(removed, " removed")
print(len(channels_seen), " channels checked")
print(len(channel_ads), " channels with ads")
