import os
import sys
from bs4 import BeautifulSoup
#import requests
#from urllib.request import urlopen
#from urllib import parse
from pathlib import Path
from tube_dl import Playlist, Youtube
#from moviepy.editor import * # stupid fucking shit

def ytplaylist(playlist='https://www.youtube.com/watch?v=SlPhMPnQ58k&list=PL4o29bINVT4EG_y-k5jGoOu3-Am8Nvi10'):
    print('Downloading...')
    #playlist += '&index=1'
    #html = requests.get(playlist, allow_redirects=True).content.decode()
    #html = urlopen(playlist).read()
    for f in os.listdir():
        if '.html' in f:
            html = open(f, 'rb').read().decode()
            search = 'Dua Lipa'
            search = 'ytd-playlist-panel-video-renderer'
            bs = BeautifulSoup(html)
            item = "yt-simple-endpoint style-scope ytd-playlist-panel-video-renderer"
            need = bs.findAll('a', {'class': item}, href=True)
            print(f'{len(need)} songs found.')
            dst = 'videos'
            index = 1
            for a in need:
                if index > 10:
                    pass#break
                href = a['href']
                print(f'{index}. {href}') 
                suff = href.split('=')[1]
                download(index, suff, dst)
                index += 1
            os.remove(f)


def progress(Chunk=None, bytes_done=None, total_bytes=None):
    till_now = bytes_done / total_bytes
    show_progress(till_now)


def show_progress(progress):
    length = 25
    block = int(round(length*progress))
    perc = round(progress*100, 2)
    if perc > 100:
        perc = 100.0
    msg = "\r[{0}] {1}%".format("#"*block + "-"*(length-block), perc)
    if progress >= 1:
        msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush() 


def download(index, url, dst):
    '''
    yt = Youtube(f'https://youtube.com/watch?v={url}')
    if 'title' not in dir(yt):
        return
    print(f'{yt.title}:', end = '\n')
    yt.formats.first().download('mp3', progress, dst, None) 
    '''
    while True:
        try:
            if 'youtube' in url:
                _, url = url.split('v=')
            elif 'youtu.be' in url:
                url = url.split('/')[-1]
            print(url)
            yt = Youtube(f'https://youtube.com/watch?v={url}')
            print(f'{index}. {yt.title}:')
            yt.formats.first().download('mp3', progress, dst, None) 
        except Exception as e:
            ##for retrying url
            #continue
            print(e)
            log = open('log.txt', 'a+')
            log.write(f'{index} : FAILED\ne\n\n')
            ok = False
            log.close()
        break


def musicyt(playlist = 'https://music.youtube.com/playlist?list=PLTy__vzNAW6C6sqmp6ddhsuaLsodKDEt_'):
    print('Downloading...')
    #playlist = 'https://music.youtube.com/playlist?list=PLhJok_NiXcsi_t9R1E8Fw5TvPdmIFf1yz' # Sam Beam
    #playlist = 'https://music.youtube.com/playlist?list=PL640399F2F8BF381C' # SAM BEAM
    playlist = 'https://music.youtube.com/playlist?list=RDCLAK5uy_nbTnrBv4CxZys35IAzhO0-fFCiKD58qzo' # Bollywood Fire
    pl = Playlist(playlist).videos
    dst = 'videos'
    #download('GifLPveCWx8', dst)
    #return
    index = 0
    for suff in pl:
        index += 1
        ok = True
        if index > 10:
            pass#break
        print(f'{index}.', end=' ')
        print(suff)
        download(index, suff, dst)


def convert():
    print('\n\nConverting...')
    src = 'videos'
    dst = 'audios'
    index = 1
    for f in os.listdir(src):
        src_path = os.path.join(src, f);
        aud_name = Path(src_path).name.split('.')[0] + '.mp3'
        dst_path = os.path.join(dst, aud_name)
        print(f'{index}. {src_path} -> {dst_path}:', end = '\n')
        os.system(f'ffmpeg -v quiet -stats -i "{src_path}" "{dst_path}"')
        '''
        if '.mp4' in f:
            # stupid shit
            vid = VideoFileClip(file_path)
            aud = videoClip.audio
            aud.write_audiofile(aud_name)
            vid.close()
            aud.close()
        '''
        index += 1

def init():
    vid_path = 'videos'
    aud_path = 'audios'
    songs_path = 'songs'
    log_file = 'log.txt'
    if os.path.exists(log_file):
        os.remove(log_file)
    if os.path.exists(songs_path):
        os.system(f'rmdir {songs_path} /s /q')
    if os.path.exists(vid_path):
        os.system(f'rmdir {vid_path} /s /q')
    if os.path.exists(aud_path):
        os.system(f'rmdir {aud_path} /s /q')
    #os.mkdir(songs_path)
    os.mkdir(vid_path)
    os.mkdir(aud_path)


if __name__ == "__main__":
    os.chdir(os.getcwd())
    init()
    print('1. Youtube Playlist')
    print('2. Youtube Music Playlist')
    print('3. Youtube Video url')
    choice = eval(input("Enter choice: "))
    if choice == 1:
        ytplaylist()
    elif choice == 2:
        url = input("Enter the url: ")
        musicyt(url)
    elif choice == 3:
        url = input("Enter the url: ")
        download(1, url, 'videos')
    convert()

