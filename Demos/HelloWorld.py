
import kivy
kivy.require('1.11.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        return Label(text='Hello world')

if __name__ == ' main ':
    MyApp().run()

# Para executar, digite:
# python HelloWorld.py