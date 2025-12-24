# this is the program to fetch lyrics for a given song. we shall utilise multithreading by using threadpoolexecutor to fetch from multiple sources
# and then compile the results to make sure the discography is consistent and without duplicates.
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed




def get_lyrics(artist_name, track_name):
    #lrclib
    def fetch_from_lrclib():
        url = "https://lrclib.net/api/get"
        params = {
            "artist_name": artist_name.strip().title(), 
            "track_name": track_name.strip().title()
        }
        try: 
            response = requests.get(url, params = params, timeout=10) # this how we making requests
            # safety check only, can remove later
            if response.status_code != 200:
                print(f"Request failed with status: {response.status_code}")
                return ("LRCLIB", None)

            
            data = response.json()
            if data.get('syncedLyrics'):
                lyrics = data["syncedLyrics"]
                source = "LRCLIB (synced)"
            elif data.get('plainLyrics'):
                lyrics = data["plainLyrics"]
                source = "LRCLIB (plain)"
            else:
                lyrics = "No lyrics in Response"
                source = None
            return ("LRCLIB", lyrics)
        except Exception as e:
            print("LRCLIB error", e)
            pass
            return ("LRCLIB", None)
    #declare two functions for netease, because you need song id to get lyrics
    headers = {
        "User-Agent" : "Mozilla/5.0",
        "Referer": "https://music.163.com"
    }

    #scrapesoft
    def fetch_from_scrapesoft():
        url = "https://scrapesoft-music-lyrics.p.rapidapi.com/lyrics"
        querystring = {"artist": artist_name, "title": track_name}
        headers_local = {
            "X-RapidAPI-Key": "7daf6176f4msh56f941e4bb36640p110601jsna22d935cf892",
            "X-RapidAPI-Host": "scrapesoft-music-lyrics.p.rapidapi.com",
        }
        try:
            response = requests.get(url, headers=headers_local, params=querystring)
            if response.status_code == 200:
                data = response.json()
                if data.get("lyrics"):
                    return ("Scrapesoft", data["lyrics"])
        except Exception as e:
            print(f"Scrapesoft API error: {e}")
        return ("Scrapesoft", None)
    

    def fetch_songid_from_netease():
        url = "https://music.163.com/api/search/get"
        params = {
            "s": f"{track_name} {artist_name}",
            "type": 1,
            "limit": 5,
            "offset": 0
        }
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            data = response.json()
            result = data.get("result", {})
            if result.get("songCount", 0) > 0:
                return result["songs"][0]["id"]
        except Exception as e:
            print(f"NetEase search error: {e}")
        return None
        
    #netease   
    def fetch_from_netease():
        song_id = fetch_songid_from_netease()
        if not song_id:
            return("NetEase", None)
        
        url = "https://music.163.com/api/song/lyric"
        params = {
            "id": song_id,
            "lv": 1,   # Get regular lyrics
            
        }
        try: 
            response = requests.get(url,params=params, headers=headers, timeout=10)
            data = response.json()
            if 'lrc' in data and 'lyric' in data['lrc'].get('lyric'):
                lyrics = data['lrc']['lyric']
                clean_lyrics = "\n".join(
                    line.split("]", 1)[-1].strip() for line in lyrics.splitlines() if "]" in line
                )
                return ("NetEase", clean_lyrics)
        except Exception as e:
            print("NetEase error:", e)
            pass
        return ("NetEase", None)
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(fetch_from_lrclib),
            executor.submit(fetch_from_netease),
            executor.submit(fetch_from_scrapesoft)
        ]
        for future in as_completed(futures):
            source, lyrics = future.result()
            if lyrics:
                return {
                    "artist": artist_name, 
                    "title": track_name, 
                    "lyrics": lyrics, 
                    "source": source
                }

    return {"artist": artist_name, "title": track_name, "lyrics": " Lyrics not found", "source": None}
    #result = fetch_from_lrclib()
    #return result

if __name__ == "__main__":
    print(get_lyrics("Kanye West", "Heartless"))