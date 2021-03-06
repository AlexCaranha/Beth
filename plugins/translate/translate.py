from yapsy.IPlugin import IPlugin
from plugins.categories import Knowledge
from googletrans import Translator
import re

class Translate(Knowledge):
    def setup(self):
        self.translator = Translator()
        print(f"Translate loaded: ok.")

    def translate_from_to(self, sentence, language_from, language_to):        
        output = self.translator.translate(sentence, src=language_from, dest=language_to)        
        translated = output.text
        return translated

    def translate_from_pt_to_en(self, sentence:str):
        output = self.translate_from_to(sentence, language_from="pt", language_to="en")
        return output

    def translate_from_en_to_pt(self, sentence:str):
        output = self.translate_from_to(sentence, language_from="en", language_to="pt")
        return output

    def is_the_question(self, pattern, input: str):
        match = re.search(pattern, input, re.IGNORECASE)
        return match.group('sentence') if match is not None else None

    def is_activated_to_answer_now(self):
        return False

    def get_message_when_plugin_activated_to_answer_now(self):
        return None

    def run(self, input):
        # English to Portuguese
        sentence = self.is_the_question(r'traduzir para o português a frase em inglês (?P<sentence>.*)', input)
        if sentence is not None:
            sentence_translated = self.translate_from_en_to_pt(sentence)
            return sentence_translated
        
        # Portuguese to English
        sentence = self.is_the_question(r'traduzir para o inglês a frase (?P<sentence>.*)', input)
        if sentence is not None:
            sentence_translated = self.translate_from_pt_to_en(sentence)            
            return sentence_translated

        return None
