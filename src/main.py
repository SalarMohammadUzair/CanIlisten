# this is the main file or orchestrator of the application.
from lyrics_fetch import get_lyrics
from file_manager import save_lyrics, save_gemini_response
from gemini_analyser import analysis
artist = input("input artist")
track = input("input track")
ans = get_lyrics(artist, track)#, formatted= True)
save_lyrics(ans['artist'], ans['title'], ans)
# print(ans)
# print(type(ans))
# ans is basically what we send to gemini so we don't really need to read the .json file. 
result = analysis(artist, ans['lyrics'])
#print("analysis result:", result)
save_gemini_response(artist, track, result)

