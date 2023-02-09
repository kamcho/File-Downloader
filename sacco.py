import os
from urllib.parse import urlparse

from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.app import App
import ctypes
import mysql.connector
from kivymd.uix.dialog import MDDialog
from pytube import YouTube, streams
from kivymd.uix.picker import MDDatePicker
from kivy.lang.builder import Builder
from kivymd.uix.button import MDRoundFlatIconButton, MDRectangleFlatButton, MDFlatButton
from kivymd.uix.screen import MDScreen,Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
from kivymd.uix.list import TwoLineIconListItem,TwoLineAvatarListItem,ImageLeftWidget,ImageRightWidget
import matplotlib.pyplot as plt
# from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from urllib.request import urlretrieve
import urllib
import time

# class Splash(Screen):
#     """This class will show the splash screen of Docto365"""
#     def on_enter(self, *args):
#         Clock.schedule_once(self.switch_to_home, 10)
#
#     def switch_to_home(self, dt):
#         self.manager.current = 'Login'
from kivymd.uix.list import OneLineListItem
class Home(Screen):
    dialog=None
    k = ObjectProperty(None)

    def get_link(self):
        CF_TEXT = 1

        kernel32 = ctypes.windll.kernel32
        kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
        kernel32.GlobalLock.restype = ctypes.c_void_p
        kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
        user32 = ctypes.windll.user32
        user32.GetClipboardData.restype = ctypes.c_void_p

        def get_clipboard_text():
            user32.OpenClipboard(0)
            try:
                if user32.IsClipboardFormatAvailable(CF_TEXT):
                    data = user32.GetClipboardData(CF_TEXT)
                    data_locked = kernel32.GlobalLock(data)
                    text = ctypes.c_char_p(data_locked)
                    value = text.value
                    kernel32.GlobalUnlock(data_locked)
                    return value
            finally:
                user32.CloseClipboard()
        k=self.k
        self.k=get_clipboard_text()

        self.show_alert_dialog()

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Download",
                text=f"{self.k.decode('utf-8')}",
                auto_dismiss=True,
                buttons=[MDFlatButton(text="Download", on_release=self.proceed ), MDFlatButton(text="Cancel", on_release=self.close_dialog),],)
        self.dialog.open()

    def finalise(self,*args):
        try:
            self.link = YouTube(self.k.decode("utf-8"))
            self.manager.current = 'Download'
            print(self.link.title)

        except:
            print("hey")
            a = urlparse(self.k.decode("utf-8"))
            print(a.path)  # Output: /kyle/09-09-201315-47-571378756077.jpg
            print(os.path.basename(a.path))
            urlretrieve(self.k.decode("utf-8"), f"E:\\pythonProject1\\SuperDownloader\\{os.path.basename(a.path)}")
    def proceed(self,*args):
        self.close_dialog()
        self.finalise()


    def close_dialog(self,*args):
        self.dialog.dismiss()
class Download(Screen):
    dialog = None
    def on_pre_enter(self):
        file=self.main.k
        file = YouTube(file.decode('utf-8'))

        print(file.title)
        self.ids.file_title.text=file.title
        self.ids.file_thumbnail.source=file.thumbnail_url
        video=file.streams.filter(type="video",adaptive=True)
        print(video)


        for res in file.streams.filter(type='video'):
            imag = ImageLeftWidget(source="IMG_20200206_175255_2.jpg")
            self.list_item = TwoLineAvatarListItem(text=f"{res.resolution  }",secondary_text=f"{res.itag}",on_release=self.get_itag)
            self.list_item.add_widget(imag)
            self.ids.container.add_widget(self.list_item)
        for res in file.streams.filter(type='audio'):
            imag = ImageLeftWidget(source="IMG_20200206_175255_2.jpg")
            self.list_item2 = TwoLineAvatarListItem(text=f"{res.abr}", secondary_text=f"{res.itag}",on_release=self.get_itag)
            self.list_item2.add_widget(imag)
            self.ids.contain.add_widget(self.list_item2)
        self.file=file

    def initiate_download(self,*args):
        self.close_dialog()
        print(self.itag)
        stream = self.file.streams.get_by_itag(self.itag)

        stream.download()

    def get_itag(self,presed):
        self.itag=presed.secondary_text
        self.text=presed.text
        self.show_alert_dialog()
        print(self.itag)
    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Download",
                text=f"{self.text}",
                buttons=[
                    MDFlatButton(
                        text="Download", on_release=self.initiate_download  # text_color=self.theme_cls.primary_color
                    ),
                    MDFlatButton(
                        text="Cancel", on_release=self.close_dialog
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self,*args):
        self.dialog.dismiss()

class WindowManager(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style="Dark"
        return Builder.load_file("main.kv")
        # dat=self.root.current_screen.ids.date
        # dat.add_widget(date_dialog)
MainApp().run()
