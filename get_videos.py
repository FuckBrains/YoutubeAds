import requests

channel_list = []


resp = requests.get('https://zummie.com/yt888/items/channel?filter[category]=3')


if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))


for item in resp.json()['data']:
    channel_list.append(item['id'])


# print(channel_list)



resp = requests.get('https://zummie.com/yt888/items/channel?filter[category]=1')


if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))


for item in resp.json()['data']:
    channel_list.append(item['id'])


video_list = []

for channel_id in channel_list:
    print("checking channel " + channel_id)
    resp = requests.get('https://zummie.com/yt888/items/video?filter[channel_id]=' + channel_id)


    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))


    for item in resp.json()['data']:
        if not item['removed']:
            video_list.append(item['video_id'])


outfile = open('conspiracy_videos.txt', 'w')
for vid in video_list:
    outfile.write(vid + '\n')


outfile.close()
print(len(video_list))
print(video_list)