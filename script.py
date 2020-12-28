import os
import sys
from bs4 import BeautifulSoup
from pathlib import Path
from tube_dl import Playlist, Youtube

def ytplaylist(playlist = None):
    print('Downloading...')
    for f in os.listdir():
        if '.html' in f:
            html = open(f, 'rb').read().decode()
            bs = BeautifulSoup(html)
            item = "yt-simple-endpoint style-scope ytd-playlist-panel-video-renderer"
            need = bs.findAll('a', {'class': item}, href=True)
            print(f'{len(need)} songs found.')
            for index, a in enumerate(need):
                href = a['href']
                print(f'{index+1}.', end = ' ') 
                suff = href.split('v=')[1]
                download(index+1, suff)
            os.remove(f)
            folder = f.split(".")[0] + "_files"
            os.system(f'rmdir "{folder}" /s /q')


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


def download(index, url, dst = 'videos'):
    while True:
        try:
            if 'youtube' in url:
                _, url = url.split('v=')
            elif 'youtu.be' in url:
                url = url.split('/')[-1]
            yt = Youtube(f'https://youtube.com/watch?v={url}')
            print(f'{yt.title}:')
            yt.formats.first().download('mp3', progress, dst, None) 
        except Exception as e:
            print(e)
            log = open('log.txt', 'a+')
            log.write(f'{index}:{url}\n{e}\n')
            ok = False
            log.close()
        break


def musicyt(playlist):
    print('Downloading...')
    pl = Playlist(playlist).videos
    for index, suff in enumerate(pl):
        ok = True
        print(f'{index+1}.', end=' ')
        download(index+1, suff)


def convert(src='videos', dst='audios'):
    print('\n\nConverting...')
    print(f'{src} -> {dst}')
    for index, f in enumerate(os.listdir(src)):
        src_path = os.path.join(src, f);
        aud_name = Path(src_path).name.split('.')[0] + '.mp3'
        dst_path = os.path.join(dst, aud_name)
        print(f'{index+1}. {aud_name}:', end = '\n')
        os.system(f'ffmpeg -v quiet -stats -i "{src_path}" "{dst_path}"')


def init():
    vid_path = 'videos'
    aud_path = 'audios'
    log_file = 'log.txt'
    if os.path.exists(log_file):
        os.remove(log_file)
    if os.path.exists(vid_path):
        os.system(f'rmdir "{vid_path}" /s /q')
    if os.path.exists(aud_path):
        os.system(f'rmdir "{aud_path}" /s /q')
    os.mkdir(vid_path)
    os.mkdir(aud_path)


def retry():
    if not os.path.exists('log.txt'):
        return
    test_path = 'retry'
    if os.path.exists(test_path):
        os.system(f'rmdir "{test_path}" /s /q')
    os.mkdir(test_path)
    log = open('log.txt', 'r').read().split('\n')
    print(log)
    for index, line in enumerate(log):
        line = line.split(':')
        if len(line) == 2:
            if 'title' in log[index+1]:
                continue
            url = line[1]
            yt = Youtube(f'https://youtube.com/watch?v={url}')
            print(f'{yt.title}:')
            yt.formats.first().download('mp3', progress, test_path, None) 
    convert(src=test_path, dst='audios')
    os.remove('log.txt')

def main():
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


if __name__ == "__main__":
    main()
    retry()

