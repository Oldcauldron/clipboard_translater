from googletrans import Translator
from loguru import logger
import pyperclip
import datetime
import pyautogui
import subprocess
import time
from synonyms import syn


pyperclip.copy('')

past = ''


def conn(past, options):
    translator = Translator()
    result = translator.translate(past, src='en', dest='ru')
    if options == "synonym":
        syndict = syn(past)
        return result, translator, syndict
    return result, translator, None


if __name__ == '__main__':

    text = f'Copy [stop] for exit, or [pause] for pause. You going to find ..'
    options = pyautogui.confirm(text=f'{text}',
                                title='choosing',
                                buttons=["translate", "synonym"])

    _, translator, _ = conn('one', None)

    while True:

        first_time = datetime.datetime.now()

        while not past:
            now = datetime.datetime.now().minute - first_time.minute
            if now >= 1:
                _, translator, _ = conn('one', None)
                first_time = datetime.datetime.now()
            time.sleep(1)
            past = pyperclip.paste()

        if past == 'pause':
            past = pyautogui.confirm(
                text='PAUSE! Please sczmack continue or stop and exit',
                title='helper', buttons=['continue', 'stop'])
            if past == 'continue':
                past = pyperclip.copy('')

        if past == 'stop':
            pyautogui.alert(f'Exit')
            break

        if type(past) == str:
            past = past.replace('\n', ' ').replace('\r', '').lower()
            try:
                # result = translator.translate(past, src='en', dest='ru')
                result, translator, syndict = conn(past, options)
            except Exception as err:
                logger.info(f'EXCEPTION - {err}')
                result, translator, syndict = conn(past, options)
            if syndict:
                text = f'synonyms of : {past}\n'
                for k, v in syndict.items():
                    text += f'{k} >>>\n {v}\n\n'
                message = pyautogui.confirm(text=f'{text}',
                                            title='synonym',
                                            buttons=[
                                                "translate",
                                                "don't translate"])
                with open('synonyms.txt', 'w') as f:
                    f.write(text)
                time.sleep(1)
                subprocess.Popen(['start', 'synonyms.txt'], shell=True)

            if not syndict or message == "translate":
                message = pyautogui.confirm(text=f'{past} - {result.text}',
                                            title='writing in file',
                                            buttons=[
                                                "write it",
                                                "don't write it"])
            if message == 'write it':
                with open('new_dict.txt', 'a') as nd:
                    writeit = f'{past}, {result.text.lower()}\n'
                    nd.write(writeit)
                    print(writeit)
        past = pyperclip.copy('')

    subprocess.Popen(['start', 'new_dict.txt'], shell=True)
