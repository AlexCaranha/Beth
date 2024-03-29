
from plugins.categories import Internal
from classes.util import is_the_question, is_the_question_with_sentence
from module import speak as gtts_speak


class Speaker(Internal):
    def setup(self):
        self.is_repeat_what_i_say_activated = True

        self.activated = True
        self.language = 'pt'
        self.default_rate = 100
        self.rate = self.default_rate

        print(f"Speaker loaded: ok.")

    def set_rate(self, rate, rate_variation):
        self.rate *= (1 + rate_variation)
        self.engine.setProperty('rate', self.rate)

    def speak(self, text):
        if not self.activated:
            return

        gtts_speak(text, self.language)

    def speak_what_i_say(self, text):
        if self.is_repeat_what_i_say_activated:
            self.speak(f"Você disse: {text}")

    def is_the_question(self, pattern, input: str, threshold=85):
        result = is_the_question(pattern, input, threshold)
        return result

    def is_the_question_with_sentence(self, pattern, input: str):
        match = is_the_question_with_sentence(pattern, input)
        return match.group('sentence') if match is not None else None

    def get_message_when_plugin_activated_to_answer_now(self):
        return None

    def is_activated_to_answer_now(self):
        return self.activated

    def run(self, input):
        if not self.activated:
            if self.is_the_question(r'silenciar assistente', input):
                self.is_repeat_what_i_say_activated = True
                self.activated = True
                return "Beth saiu do modo de silêncio."

            return None

        if self.is_the_question(r'', input):
            self.is_repeat_what_i_say_activated = False
            self.activated = False
            return "Beth entrou em modo de silêncio."

        if self.is_the_question(r'normalizar velocidade', input):
            self.set_rate(self.default_rate)
            return f"velocidade do áudio normalizada."

        percentual = self.is_the_question_with_sentence(
            r'aumentar a velocidade em (?P<sentence>.*)%', input)

        if percentual is not None:
            self.set_rate(None, +(int(percentual) / 100))
            return f"velocidade do áudio aumentada em {percentual}%."

        percentual = self.is_the_question_with_sentence(
            r'diminuir a velocidade em (?P<sentence>.*)%', input)

        if percentual is not None:
            self.set_rate(None, -(int(percentual) / 100))
            return f"velocidade do áudio reduzida em {percentual}%."

        return None
