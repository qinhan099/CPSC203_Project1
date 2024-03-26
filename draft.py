import pandas as pd
from dataclasses import dataclass, field, asdict
from typing import List, Tuple
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import billboard
from collections import defaultdict, Counter
from models import *
import config


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.CLIENT_ID,
                                                           client_secret=config.CLIENT_SECRET))




"""
PART 1: Getting the Top 100 Data!
You must complete Part 1 before moving on down below
"""
def getPlaylist(id: str) -> List[Track]:
    # fetch tracks data from spotify given a playlist id
    playlistdata = sp.playlist(id)
    tracks = playlistdata['tracks']['items']
    track_ids = [ item['track']['id'] for item in tracks]
    audio_features = sp.audio_features(track_ids)
    audio_info = {}  # Audio features list might not be in the same order as the track list
    for af in audio_features:
        audio_info[af['id']] = AudioFeatures(af['danceability'],
                                             af['energy'],
                                             af['key'],
                                             af['loudness'],
                                             af['mode'],
                                             af['speechiness'],
                                             af['acousticness'],
                                             af['instrumentalness'],
                                             af['liveness'],
                                             af['valence'],
                                             af['tempo'],
                                             af['duration_ms'],
                                             af['time_signature'],
                                             af['id'])

    # prepare artist dictionary
    # we can use set() to build unique() values as the nature of this data type, avoid using same name comparisons.
    artist_ids = [] # ToDo: make a list of unique artist ids from tracks list
    for item in tracks:
        artists = item['track']['artists']
        for seq in artists:
            artist_id = seq['id']
            artist_ids.append(artist_id)
    artist_ids = list(set(artist_ids))


    artists_list = {}
    for k in range(1+len(artist_ids)//50): # can only request info on 50 artists at a time!
        artists_response = sp.artists(artist_ids[k*50:min((k+1)*50,len(artist_ids))]) #what is this doing?
        for a in artists_response['artists']:
            artists_list[a['id']] = Artist(a['id'], 
                                      a['name'], 
                                      a['genres'])# TODO: create the Artist for each id (see audio_info, above)

    # populate track dataclass
    trackList = [ Track(id= item['track']['id'], 
                       name= item['track']['album']['name'],
                       artists= [artists_list[seq['id']] for seq in item['track']['artists']], # I want to pass artist Object here, where if there's two artist, pass a list of two, if one, pass a list of one.
                       audio_features= audio_info[item['track']['id']]) for item in tracks]

    return trackList


def getHot100() -> List[Track]:
    # Billboard hot 100 Playlist ID URI
    hot_100_id = "6UeSakyzhiEt4NB3UAd6NQ"
    return getPlaylist(hot_100_id)

# ---------------------------------------------------------------------

"""
Part 2: The Helper Functions
Now that we have the billboard's top 100 tracks, let's design some helper functions that will make our lives easier when creating our dataframe.
"""

def getGenres(t: Track) -> List[str]:
    '''
    Takes in a Track and produce a list of unique genres that the artists of this track belong to
    '''
    genre_list =[]
    for artist in t.artists:
        for seq in artist.genres:
            genre_list.append(seq)

    return list(set(genre_list))

def doesGenreContains(t: Track, genre: str) -> bool:
    '''
    TODO
    Checks if the genres of a track contains the key string specified
    For example, if a Track's unique genres are ['pop', 'country pop', 'dance pop']
    doesGenreContains(t, 'dance') == True
    doesGenreContains(t, 'pop') == True
    doesGenreContains(t, 'hip hop') == False
    '''
    genre_list = getGenres(t)
    genre_accumulator = []
    for item in genre_list:
        if genre in item:
            genre_accumulator.append(1)
        else:
            genre_accumulator.append(0)
    
    if 1 in genre_accumulator:
        return True
    else:
        return False

def getTrackDataFrame(tracks: List[Track]) -> pd.DataFrame:
    '''
    This function is given.
    Prepare dataframe for a list of tracks
    audio-features: 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                    'duration_ms', 'time_signature', 'id', 
    track & artist: 'track_name', 'artist_ids', 'artist_names', 'genres', 
                    'is_pop', 'is_rap', 'is_dance', 'is_country'
    '''
    # populate records
    records = []
    for t in tracks:
        to_add = asdict(t.audio_features) #converts the audio_features object to a dict
        to_add["track_name"] = t.name
        to_add["artist_ids"] = list(map(lambda a: a.id, t.artists)) # we will discuss this in class
        to_add["artist_names"] = list(map(lambda a: a.name, t.artists))
        to_add["genres"] = getGenres(t)
        to_add["is_pop"] = doesGenreContains(t, "pop")
        to_add["is_rap"] = doesGenreContains(t, "rap")
        to_add["is_dance"] = doesGenreContains(t, "dance")
        to_add["is_country"] = doesGenreContains(t, "country")
        
        records.append(to_add)
        
    # create dataframe from records
    df = pd.DataFrame.from_records(records)
    return df

# ---------------------------------------------------------------------
# The most popular artist of the week

def artist_with_most_tracks(tracks: List[Track]) -> (Artist, int): # type: ignore
    '''
    TODO
    List of tracks -> (artist, number of tracks the artist has)
    This function finds the artist with most number of tracks on the list
    If there is a tie, you may return any of the artists
    '''         
    tally = Counter() # these structures will be useful!
    for track in tracks:
        for artist in track.artists:
            tally[artist.name] += 1
    arts = dict(tally)
    top_artist = max(arts, key=arts.get)
    return top_artist



"""
Part 3: Visualizing the Data
"""

# 3.1 scatter plot of dancability-speechiness with markers colored by genre: is_rap
                       
def danceability_plot(tracks: List[Track]):
    df = getTrackDataFrame(tracks)
    # Filter out the rap genre
    rap_tracks = df[df['is_rap'] == True]

    # Set danceability frame and speechiness frame individually.
    danceability = rap_tracks['danceability']
    speechiness = rap_tracks['speechiness']
    # Create scatter plot figure and render our data on it.
    plt.scatter(x=danceability, y=speechiness, color='blue', label='Rap', alpha=0.5)

    #Configure the plot
    plt.title('Danceability vs. Speechiness by Genre')
    plt.xlabel('Danceability')
    plt.ylabel('Speechiness')
    plt.legend()
    plt.grid(True)

    plt.show()


    #TODO assemble a scatter plot using the audio characteristics of the songs

# 3.2 scatter plot (ask your own question). 
# Now I want to plot the energy and danceability plot comparison with the catergory pop.
    
def energy_plot(tracks: List[Track]):
    df = getTrackDataFrame(tracks)
    # Filter out the rap genre
    pop_tracks = df[df['is_pop'] == True]

    # Set danceability frame and speechiness frame individually.
    danceability = pop_tracks['danceability']
    energy = pop_tracks['energy']
    # Create scatter plot figure and render our data on it.
    plt.scatter(x=danceability, y=energy, color='red', label='Pop', alpha=0.5)

    #Configure the plot
    plt.title('Danceability vs. Energy in Pop Genre')
    plt.xlabel('Danceability')
    plt.ylabel('Energy')
    plt.legend()
    plt.grid(True)

    plt.show()



# ---------------------------------------------------------------------

tracks_df = getPlaylist('https://open.spotify.com/playlist/37i9dQZF1DWTvNyxOwkztu?si=023b6aa48e7f47cf')
instance = tracks_df[0]
print(energy_plot(tracks_df))