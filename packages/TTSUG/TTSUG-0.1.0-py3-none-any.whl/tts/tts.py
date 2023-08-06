import requests
import time

class TTSClass:
    def __init__(self, msg="", lang='en'):
        self.msg = msg
        self.lang = lang
        self.convert_text_to_speech()

    def convert_text_to_speech(self):
        if self.msg == "":
            raise Exception('Parameter is Blank !!!')

        message_string = self.msg
        encoded_str = message_string.replace(" ", "+")
        lang = self.lang

        if len(encoded_str) > 100:
            raise Exception('Parameter is more than 100 character.')

        url = f'https://translate.google.com/translate_tts?ie=UTF-8&tl={lang}&client=tw-oa&q={encoded_str}'
        r = requests.get(url)
        current_date_and_time_string = str(time.strftime("%Y%m%d-%H%M%S"))
        extension = ".mp3"
        file_name = current_date_and_time_string + extension
        open(file_name, 'wb').write(r.content)
        return True
