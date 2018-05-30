from bs4 import BeautifulSoup
import requests
import urllib.parse

access_token = 'some access token'
user_id = 'some username/user_id'
authorization_header = {"Authorization": "Bearer {}".format(access_token)}

try:
    html_request = requests.get('https://www.billboard.com/charts/hot-100')
    top_songs = html_request.text
except:
    print('error getting songs')

soup = BeautifulSoup(top_songs, 'html.parser')
song_data = {}
fav_artists = ['drake', 'zedd', 'the weeknd', 'shawn mendes', 'ariana grande']


def songs_of_artist(artist_list, artist):
    if any(artist in s for s in artist_list):
        return True
    else:
        return False


def find_song_id(name):
    params = '?q={}&type=track&market=US&limit=1'.format(urllib.parse.quote(name))
    response = requests.get('https://api.spotify.com/v1/search' + params, headers=authorization_header)
    result = response.json()
    song_id = ''
    for track in result['tracks']['items']:
        artist = track['artists'][0]['name']
        for key, val in song_data.items():
            if artist.lower().strip() == val:
                song_id = track['id']
    return song_id


for song_html in soup.find_all('div', class_='chart-row__title'):
    song_name = song_html.h2.text.strip()
    for link in song_html.select('a'):
        song_artist = link.text.strip().lower()
        if songs_of_artist(fav_artists, song_artist) is True:
            song_data[song_name] = song_artist

song_ids = []
for name, artist in song_data.items():
    song_ids.append(find_song_id(name))


def create_playlist():
    playlist_name = 'Scripted Playlist'
    header = {'Authorization': 'Bearer {}'.format(access_token), 'Content-Type': 'application/json'}
    body = {'name': playlist_name, 'description': 'Auto generated Billboard hot 100 playlist'}
    new_playlist_id = ''
    response = requests.post('https://api.spotify.com/v1/users/{}/playlists'.format(user_id), headers=header, json=body)
    if response.status_code in [200, 201]:
        new_playlist_id = response.json()['id']
    if add_to_playlist(new_playlist_id):
        print('Completed')
    else:
        print('Unsuccessful')


def add_to_playlist(playlist_id):
    header = {'Authorization': 'Bearer {}'.format(access_token), 'Content-Type': 'application/json'}
    body = {'uris': list(map((lambda songId: 'spotify:track:' + songId), song_ids))}
    requests.post('https://api.spotify.com/v1/users/{}/playlists/{}/tracks'.format(user_id, playlist_id),
                      headers=header, json=body)
    return True


create_playlist()
