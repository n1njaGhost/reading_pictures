from itertools import count
from sys import argv
import cv2
import pytesseract
import clipboard
import os
import shutil


class ReadingText:

    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    folder_path = 'img/'

    def mode():
        if len(argv) == 1 or argv[1] == 'scan':
            ReadingText.__parsingPhotos()
        elif argv[1] == 'clear':
            ReadingText.__clearFolder()
        else:
            return 0

    def __textRecognition(path):  # Зчитує текст з картинки
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cfg = r'--oem 3 --psm 6'

        return pytesseract.image_to_string(img, config=cfg)

    def __resultsHandler(path):  # Чистить код з __textRecognition() від лишніх пробілів
        source_code = ReadingText.__textRecognition(path)
        source_code = (' '.join(map(str, source_code.split('  ')))
                       ).replace('\n\n', '\n').replace(' ;', ';').replace('"', "'").replace('’', "'").replace('I5', 'IS')

        return source_code

    def __parsingPhotos():  # Перебирає всі картинки в папці
        result = ''
        list_photo_names = os.listdir(ReadingText.folder_path)

        if not list_photo_names:
            return print(None)

        for screenshot in list_photo_names:
            if '.png' in screenshot:
                result += ReadingText.__resultsHandler(
                    ReadingText.folder_path + screenshot) + '\n'

        clipboard.copy(result)  # Копіює в буфер
        print(result)
        ReadingText.__clearFolder()

    def __clearFolder():
        shutil.rmtree(ReadingText.folder_path)
        os.mkdir(ReadingText.folder_path)
