#import kivy
# kivy.require('2.0.0')
#import kivymd
import googletrans
from googletrans import Translator
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.image import Image
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

# import translate
# import googletrans
# from googletrans import Translator
Window.size = (300, 500)


class ConverterApp(MDApp):

    def on_solution(self, instance):

        field_data = self.input.text
        if len(field_data) >= 1:
            # print("Field data was", field_data)
            trans = Translator()
            detecting_language = trans.detect(self.input.text)
            language_type = googletrans.LANGUAGES[detecting_language.lang]
            destination_type = googletrans.LANGUAGES['en']
            # print("Language is",language_type)
            translated = trans.translate(self.input.text, src=detecting_language.lang, dest="en").text
            # print("source data",self.text_inp.text)
            # print("desti data",translated)
            self.final_string = "Details" + "\n" + "------------" + "\n" + "Source text-  " + self.input.text + "\n" + "Source language-  " + language_type + "\n" + "Destination text-  " + translated + "\n" + "Destination lang-  " + destination_type + "\n"
            self.input.text = self.final_string
        else:  ## here we need to create dialog box
            self.close_button = MDFlatButton(text="Ok", on_release=self.close_dialog)
            self.dialog = MDDialog(
                text="Please enter some text",
                buttons=[self.close_button
                         # MDFlatButton(
                         #     text="Ok",
                         #     theme_text_color="Custom",
                         #     size_hint=(0.7,1),
                         #     on_release=self.close_dialog
                         # text_color=self.theme_cls.primary_color

                         ]
            )
            self.dialog.open()
            # self.text_inp.text = "You entered empty text, Please Enter text"
        # btn=Button(text="convert")

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def build(self):
        self.state = 0  # initial state
        self.theme_cls.primary_palette = "Pink"
        screen = MDScreen()
        self.th_sc_layout = MDBoxLayout(orientation='vertical')
        # Box layout

        # top toolbar
        self.toolbar = MDToolbar(title="Language Translator")
        self.toolbar.pos_hint = {"top": 0}
        # self.toolbar.size_hint = (0.8,1)
        # self.toolbar.size_hint=(0.2,0.2)
        self.toolbar.right_action_items = [
            ["clock", lambda x: True]]
        self.toolbar.left_action_items = [
            ["menu", lambda x: True]]
        self.th_sc_layout.add_widget(self.toolbar)

        self.input = TextInput(hint_text="Please enter some text here")
        self.th_sc_layout.add_widget(self.input)

        # "CONVERT" button
        self.th_sc_layout.add_widget(MDFillRoundFlatButton(
            text="    Translator    ",
            font_size=25,
            pos_hint={"center_x": 0.5, "center_y": 0.15},
            on_press=self.on_solution
        ))
        screen.add_widget(self.th_sc_layout)

        return screen


if __name__ == '__main__':
    ConverterApp().run()
