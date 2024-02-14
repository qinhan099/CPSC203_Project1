# Project 1 -- Billboard 

Learning objectives:

- Use pandas data frames as a fundamental structure
- Filter, project, reassemble data frames to extract information
- Report and visualize information using a variety of plots

In class we explored one technique for extracting data from a web page, and in this project you'll use something a little bit different.
Rather than using data from Billboard, we will use a library called `Spotipy`, which makes accessing Spotify data very simple. 
This project uses `Spotipy` to not only get the rankings, but also audio features about these songs!

### Part 0 -- Getting the Code

In this repository you'll find the skeleton python files in which you should build your solutions.

### Part 1 -- Getting started

In this project, we will use the (free) [Spotify Web API](https://developer.spotify.com/documentation/web-api/). It provides a set of endpoints for us to query a wide variety of aggregated information about songs, albums, artists, playlists, and more! Here is a link to the complete [Spotify API reference](https://developer.spotify.com/documentation/web-api/reference/) We encourage you to explore the API and maybe build a side project with it if you'd like! 

To access the endpoints, you will need a Spotify developer account:
- Step 1. Create a **free** [Spotify account here](https://accounts.spotify.com/en/login) and login.

- Step 2. Go to [Spotify developer Dashboard page](https://developer.spotify.com/dashboard). Follow the instructions to accept the terms of conditions.

- Step 3. Once on the [Dashboard](https://developer.spotify.com/dashboard) page, choose `Create an app` and give your project a name and a description. The Redirect URI should be set to "https://spotify.com", choose "Web API", and technique agree with the developer terms of service, and click Save. You may leave the other fields blank.

- Step 3. On the app dashboard, navigate to the "Settings" and under "Basic Information, you should see your app's `Client ID`. Your app's `Client Secret` is hidden by default, but you can display it by clicking on "View Client Secret".
    - The client ID and secret are essentially a username and password for your app to use the API.

- Step 4. Create a new file `config.py` witht he following contents:
```
# spotipy wraps the official spotify api providing simple python functions.
# TODO: Replace these two variables with the client_id and client_secret that you generated
CLIENT_ID = "fdgdfg"
CLIENT_SECRET = ""
```

- Step 5. Copy your `Client ID` and `Client Secret` to the first `# TODO` in `config.py` (which will contain your secret keys); note that you will not be able to commit changes to this file because we only want the token and key to be stored locally on your machine rather than pushed up to the cloud!

All set! Now we can start querying from Spotify using `Spotipy`!

### Part 2 -- Organizing the data

In this part of the project you will be completing the code that we began writing in `spot.py`.
Throughout that file you will see comments labeled "`TODO`".
In each  of those locations, you should either complete our code, or completely write your
own.
The dataclasses you'll use can be found in a file called `models.py`. 

Complete the following function:

- `def getPlaylist(id: str) -> list[Track]:` which queries spotify and assembles the data into a list of `Track` objects. 
As you write this code, you should scrutinize the results of the spotify queries.
They are quite complex -- part of your task is to extract the essential (and much simpler) information.

Write the following two functions:

- `getGenres(t: Track) -> list[str]` which takes in a `Track` and produce a list of unique genres that the artists of this track belong to.

- `doesGenreContains(t: Track, genre: str) -> bool` which checks if the genres of a `Track` contains the key string specified

We will use these functions to assemble a list of `Track` into a `DataFrame` containing various information about the tracks.

### Part 2 -- The most popular artist of the week

In this section, we would like to find out the most popular artist of the week. We could measure popularity by the total number of tracks that an artist has on the Billboard Hot 100 list. 

Write the function:
- `artist_with_most_tracks(tracks: list[Track]) -> (Artist, int)` which takes in a list of tracks and produce the artist and the number of tracks the artist has on the list.


### Part 3 -- Visualizing the data 

In this section, we would like to explore the audio features that each track has and how they are related to a track's genres.
A list of what these audio features represent can be found [here](https://developer.spotify.com/documentation/web-api/reference/get-audio-features).

- Write a function called `danceability_plot(tracks: list[Track]) -> matplotlib.pyplot`  that returns a scatter plot. The plot should display all the tracks with `"danceability"` as x-axis and `"speechiness"` as y-axis. Color the dots based on whether the track `"is_rap"`. Label the axes of the plot and add a legend. 

Note that we cannot autograde this function.
Please call the function, and show your plot within the `main` function in `spot.py`. 
