infile = open('chan_2_vec_categories.txt', 'r')
outfile = open('conspiracy_channels.txt','w')

seen = {}

for line in infile:
	line = line.strip().split()
	if ('Conspiracy' in line) or ('QAnon' in line):
		if float(line[3]) > .75:
			if line[0] not in seen:
				seen[line[0]] = 1
				outfile.write(line[0] + '\n')


infile.close()
outfile.close()