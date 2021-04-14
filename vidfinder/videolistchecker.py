infile = open("chan_2_vec_videos.txt", 'r')
video_list = {}
for line in infile:
    if line.strip() == "#NAME?":
        continue
    if line.strip() in video_list:
    	video_list[line.strip()] += 1
    else:
    	video_list[line.strip()] = 1

for key in video_list:
	if video_list[key] > 1:
		print(key, video_list[key])
print(video_list)