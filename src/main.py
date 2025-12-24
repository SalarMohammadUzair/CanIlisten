# this is the main file or orchestrator of the application.
from lyrics_fetch import get_lyrics
artist = input("input artist")
track = input("input track")
ans = get_lyrics(artist, track, formatted= True)
print(ans)
