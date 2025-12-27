# this is the main file or orchestrator of the application.
from lyrics_fetch import get_lyrics
from file_manager import save_lyrics, save_gemini_response
from gemini_analyser import analysis
import time
artist = input("input artist: ")
track = input("input track: ")
print("fetching lyrics")
start = time.time()
ans = get_lyrics(artist, track)#, formatted= True)
lyrics_time = time.time() - start
if ans['source'] is None:
    print(" No lyrics found")
    exit()
print(f" fetched in: {lyrics_time:.2f}s")

save_lyrics(ans['artist'], ans['title'], ans)
# print(ans)
# print(type(ans))
# ans is basically what we send to gemini so we don't really need to read the .json file. 
print("analysing lyrics")
start = time.time()
result = analysis(artist, ans['lyrics'])
analysis_time = time.time() - start
if result is None:
    print("gemini failed")
    exit()
print(f"analysed in: { analysis_time:.2f}s")
print("analysis result:", result)
save_gemini_response(artist, track, result)

