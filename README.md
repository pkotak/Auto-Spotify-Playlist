# Auto-Spotify-Playlist

The code when executed parses billboard's hot 100 chart and selects songs of my favorite artists and adds these songs to a playlist on spotify.

## Flow of the program

* Firstly we need to ensure that we have a valid spotify access token. Visit https://beta.developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow for more details.
* The program proceeds by scraping through billboard's hot 100 chart link https://www.billboard.com/charts/hot-100 . While scraping only the songs containing my favorite artists will be stored. The favorite artist list can be modified from inside the code. 
* Using the spotify's api, I find all the track ID's and store them.
* Passing the track ID's as input, I create a new playlist and add the tracks to the newly created playlist. 
* Below is the final result

![Spotify Playlist generated from using the code](https://github.com/pkotak/Auto-Spotify-Playlist/blob/master/screenshots/spotify.png)