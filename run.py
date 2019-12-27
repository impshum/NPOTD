import configparser
from requests import get
from datetime import datetime, timedelta
import os
#from multiprocessing.pool import ThreadPool


class C:
    W, G, R, P, Y, C = '\033[0m', '\033[92m', '\033[91m', '\033[95m', '\033[93m', '\033[36m'


def write_image(fname, img):
    with open(fname, 'wb') as f:
        f.write(img.content)


def get_image(url, fname, exists, single_mode, archive_mode):
    img = get(url)
    if exists and single_mode and not archive_mode:
        os.remove(fname)
        write_image(fname, img)
        return True
    elif not exists and single_mode or not exists and not single_mode:
        write_image(fname, img)
        return True


def npotd(nasa_api_key, download_dir, archive_mode, test_mode, single_mode, hd_mode, days):
    now = datetime.today().date()

    for day in range(days):
        if day > 0:
            now = now - timedelta(days=1)
        npotd_date = now.strftime('%Y-%m-%d')
        #npotd_date = now.strftime('2019-12-21')
        data = get(f'https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}&date={npotd_date}').json()

        if data.get('code'):
            print(data['code'], data['msg'])
            exit()

        r = C.R
        type = data['media_type']
        title = data['title']
        if type == 'image':
            date = data['date']
            url = data['url']
            if hd_mode:
                url = data['hdurl']
            ext = os.path.splitext(url)[1]
            fname = f'{download_dir}{date}{ext}'
            exists = os.path.isfile(fname)

            r = C.Y
            if exists and not single_mode or not exists and single_mode or not exists and not single_mode:
                if get_image(url, fname, exists, single_mode, archive_mode):
                    r = C.G

        print(f'{r}{npotd_date} {type} {title}{C.W}')


def main():
    config = configparser.ConfigParser()
    config.read('conf.ini')
    nasa_api_key = config['nasa']['nasa_api_key']
    download_dir = config['settings']['download_dir']
    single_mode = config['settings'].getboolean('single_mode')
    hd_mode = config['settings'].getboolean('hd_mode')
    archive_mode = config['archive'].getboolean('archive_mode')
    days = int(config['archive']['archive_days']) if archive_mode else 1
    test_mode = config['settings'].getboolean('test_mode')

    test_msg = f'{C.R}TEST MODE{C.Y}' if test_mode else f'{C.G}LIVE MODE{C.Y}'
    hd_msg = f'{C.P}HQ{C.Y}' if hd_mode else f'{C.P}LQ{C.Y}'

    if single_mode:
        msg = f'{C.P}SINGLE {hd_msg}{C.Y}'
    elif archive_mode:
        msg = f'{C.P}ARCHIVE {hd_msg}{C.Y}'
    else:
        msg = f'{C.P}COLLECT {hd_msg}{C.Y}'

    print(f"""{C.Y}
╔╗╔╔═╗╔═╗╔╦╗╔╦╗  {test_msg}
║║║╠═╝║ ║ ║  ║║  {msg}
╝╚╝╩  ╚═╝ ╩ ═╩╝  {C.C}v1.0 {C.G}impshum{C.W}
    """)

    npotd(nasa_api_key, download_dir, archive_mode,
          test_mode, single_mode, hd_mode, days)


if __name__ == '__main__':
    main()
