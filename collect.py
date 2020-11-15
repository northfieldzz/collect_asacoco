import csv
from googleapiclient.discovery import build
import urllib.error
import urllib.request

API_KEY = ''
v1_play_list = 'PLw58RgSzDmjr7hbo0zrfaQ027uMc6WHfO'
v2_play_list = 'PLw58RgSzDmjo2vyCbQinleQXKUyewSO9O'


def download_file(url, dl_path):
    try:
        with urllib.request.urlopen(url) as web_file:
            data = web_file.read()
            with open(dl_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
        print(e)


with open('collect.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    headers = ['thumbnail', 'title', 'published_date', 'actual']
    writer.writerow(headers)

    youtube_service = build('youtube', 'v3', developerKey=API_KEY)

    for play_list_id in [v1_play_list, v2_play_list]:
        next_page_token = None
        while True:
            condition = {}
            if next_page_token:
                condition['pageToken'] = next_page_token
                next_page_token = ''
            search_response = youtube_service.playlistItems().list(
                playlistId=play_list_id,
                part='snippet',
                maxResults=50,
                **condition
            ).execute()

            for item in search_response['items']:
                dl_path = f'./images/{item["id"]}.png'
                download_file(item['snippet']['thumbnails']['high']['url'], dl_path)
                writer.writerow([
                    dl_path,
                    item['snippet']['title'],
                    item['snippet']['publishedAt'],
                    item['snippet']['publishedAt']
                ])
            next_page_token = search_response.get('nextPageToken')
            if next_page_token is None:
                break
    else:
        print('process is end !!!')
