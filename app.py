import itertools
import os
from pathlib import Path
from datetime import datetime, timedelta

import cv2
import requests

import dotenv
dotenv.load_dotenv()

API_URL: str = 'http://localhost:5000/api/update-bin'
BIN_ID: int = int(os.environ.get('BIN-ID', 1))
files = [str(path.resolve()) for path in Path('./img').glob('*.[jpg][png][jpeg]')]
DEMO_FILES = itertools.cycle(files)
DELAY: int = 10000  # Delay in ms


def post_update(img):
    img = cv2.imencode('.jpg', img)[1]
    requests.post(API_URL, data={'id': BIN_ID}, files={'file': img})


def get_image():
    if os.environ['DEMO_MODE']:
        # print(os.listdir('./img'))
        fp = next(DEMO_FILES)
        return cv2.imread(fp)
    else:
        cam = cv2.VideoCapture(0)
        ret, img = cam.read()
        cam.release()
        return img


if __name__ == '__main__':
    try:
        print(f'Starting bin {BIN_ID}')
        window = cv2.namedWindow('Bin', cv2.WINDOW_NORMAL)
        while True:
            img = get_image()
            cv2.imshow('Bin', img)
            post_update(img)
            print(f'Next update: {datetime.now() + timedelta(milliseconds=DELAY)}')
            cv2.waitKey(DELAY)
    finally:
        cv2.destroyAllWindows()
