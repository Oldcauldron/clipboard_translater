from googletrans import Translator
from loguru import logger
import pyperclip
import datetime
import pyautogui
import subprocess
import time

translator = Translator()

pyperclip.copy('')
past = ''


def conn(past):
    translator = Translator()
    result = translator.translate(past, src='en', dest='ru')
    return result, translator


while True:

    first = datetime.datetime.now()

    while not past:
        now = datetime.datetime.now().minute - first.minute
        if now == 1:
            _, translator = conn('one')
            first = datetime.datetime.now()
        time.sleep(1)
        past = pyperclip.paste()

    if past == 'stop':
        pyautogui.alert(f'Exit')
        break

    if type(past) == str:
        past = past.replace('\n', ' ').replace('\r', '').lower()
        try:
            result = translator.translate(past, src='en', dest='ru')
        except Exception as err:
            logger.info(f'EXCEPTION - {err}')
        finally:
            result, translator = conn(past)
        message = pyautogui.confirm(text=f'{past} - {result.text}',
                                    title='writing in file',
                                    buttons=["write it", "don't write"])
        if message == 'write it':
            with open('new_dict.txt', 'a') as nd:
                writeit = f'{past}, {result.text.lower()}\n'
                nd.write(writeit)
                print(writeit)
    past = pyperclip.copy('')

subprocess.Popen(['start', 'new_dict.txt'], shell=True)


