import youtube_dlc
import json
import time
import random
import os
import sys


def download_video(download_opts,urlnum,urllist):
    with youtube_dlc.YoutubeDL(download_opts) as ydl:
        i = 0
        for url in urllist:
            while True:
                try:
                    ydl.extract_info(url, download=True)
                    wait_time(5, 20)                    
                except KeyboardInterrupt:
                    print("\nKeyboardInterrupt")
                    exit(1)
                except youtube_dlc.utils.YoutubeDLError:
                    youtube_dlc.utils.std_headers['User-Agent']=youtube_dlc.utils.random_user_agent()
                    wait_time(1, 10)
                except:
                    print("\nother error")
                    exit(1)
                else:
                    youtube_dlc.utils.std_headers['User-Agent']=youtube_dlc.utils.random_user_agent()
                    i += 1
                    print(
                        "\n\nDownloaded Items " + str(i) + "/" + str(urlnum) + "\n\n"
                        "--------------------------------------------------------------"
                    )
                    break

def flat_playlist(flat_list):
    with youtube_dlc.YoutubeDL(flat_list) as ydl:
        try:
            info_dict = ydl.extract_info(playlist, download=False)
        except youtube_dlc.utils.YoutubeDLError:
            print("\nNot get playlist. Check playlist-id and retry")
            exit(1)
        except:
            print("\nother error")
            exit(1)
        o = json.loads(json.dumps(info_dict, ensure_ascii=False))
    urllist = []
    for items in o["entries"]:
        urllist.append("https://www.youtube.com/watch?v=" + items["id"])
    urlnum = len(urllist)
    return urlnum, urllist

def wait_time(s, e):
    sleeptime = random.randrange(s, e) + random.random()
    print("wait for " + str(f"{sleeptime:.1f}"))
    time.sleep(sleeptime)


if __name__ == "__main__":

    try:
        playlist = "https://www.youtube.com/playlist?list="+sys.argv[1]
        outputpath = "./"+sys.argv[2]
    except IndexError:
        print("Arguments are playlist-id output-path")
        exit(1)


    if not os.path.exists(outputpath):
        print("Make output directory --> " + outputpath)
        os.makedirs(outputpath)


    flat_list = {
        "extract_flat": True,
    }
    urlnum,urllist=flat_playlist(flat_list)

    print(
        "--------------------------------------------------------------\n"
        "\ndownload items " + str(urlnum) + "\n"
        "download start\n\n"
        "--------------------------------------------------------------"
    )


    download_opts = {
        "format": "bestaudio/best",
        "outtmpl": outputpath + "/%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "256",
            }
        ],
    }
    download_video(download_opts,urlnum,urllist)

    print("\nDownload complete\n")
