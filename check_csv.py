import csv

filename = 'youtube_ads_test_9.csv'
infile = open(filename, newline = '', encoding = 'utf-8')
reader = csv.DictReader(infile)

count = 0
advertisers = 0
removed = 0

for row in reader:
	count += 1
	if row['advertiser']: 
		advertisers += 1
	if row['removed'] == 'True':
		removed += 1

print(count)
print(advertisers)
print(removed)