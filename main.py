import pygame.mixer_music
from kivy.config import Config
Config.set('graphics', 'resizable', 0)
from kivy.core.window import Window
Window.size = (400, 400)
import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from pygame import mixer
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder
from kivy.uix.popup import Popup



from kivy.core.window import Window
Window.clearcolor = (0.85, 0.85, 0.85, 1)

class RV(RecycleView):
    def __init__(self):
        super().__init__()

class SelectableButton(Button):
    def on_enter(self):
        Music.selected_music = self.text

Builder.load_string(
    '''<SelectableButton>:
    on_press: root.on_enter()
    
<RV>:
    viewclass: "SelectableButton"
    scroll_type: ['bars', 'content']
    size_hint: (1, 0.6)
    pos_hint: {'x': 0, 'y': 0.3}
    bar_width: 4
    bar_color: (0, 0, 0, 1)
    bar_inactive_color: (0, 0, 0, 1)
    smooth_scroll_end: 10
    always_overscroll: False
    RecycleBoxLayout:
        spacing: 1
        default_size: None, None
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: "vertical"''')


class Music(App):
    def build(self):
        # Главное окно
        self.fl = FloatLayout()
        # окно для Popup
        self.PopupWindow = FloatLayout()
        # Находится ли трек в паузе False == Nope, True == Yes
        self.playing_state = False


        # Fake icon
        self.fakePlaylist = Button(text="", size_hint=(0.15, 0.15), pos_hint={'x': 0.255, 'y': 0.125},
                                  background_normal='image/playlist.png', border=(0, 0, 0, 0),
                                  background_down='image/playlist.png')

        self.fakeRec = Button(text="", size_hint=(0.15, 0.15), pos_hint={'x': 0.595, 'y': 0.125},
                             background_normal='image/rec.png', border=(0, 0, 0, 0),
                             background_down='image/rec.png')

        self.fakesearch = Button(text="", size_hint=(0.15, 0.15), pos_hint={'x': 0.045, 'y': 0.125},
                                background_normal='image/search.png', border=(0, 0, 0, 0),
                                background_down='image/search.png')

        self.fakesetting = Button(size_hint=(0.15, 0.15), pos_hint={'x': 0.805, 'y': 0.125},
                                 background_normal='image/settings.png', border=(0, 0, 0, 0),
                                 background_down='image/settings.png')

        self.fakemusic = Button(text="", size_hint=(0.15, 0.15), pos_hint={'x': 0.420, 'y': 0.125},
                               background_normal='image/music.png', border=(0, 0, 0, 0),
                               background_down='image/music.png')

        # Вход виджеты
        self.textLogin = Label(text="Вход в аккаунт", pos_hint={'x': 0.35, 'y': 0.8}, size_hint=(0.25, 0.25),
                               font_size='30sp', color=[196, 196, 196, 1])

        self.inputLogin = TextInput(text="Логин", size_hint=(0.7, 0.08), pos_hint={'x': 0.15, 'y': 0.7})

        self.inputLogin2 = TextInput(text="Пароль", size_hint=(0.7, 0.08), pos_hint={'x': 0.15, 'y': 0.5})

        self.btnLogin = Button(text="Вход", size_hint=(0.45, 0.1), pos_hint={'x': 0.275, 'y': 0.2},
                               on_press=self.autorization)

        self.checklog1 = CheckBox(pos_hint={'x': 0.15, 'y': 0.375}, size_hint=(0.025, 0.08), color=[1, 0, 0, 1])

        self.lblreg1 = Label(text="Запомнить меня", pos_hint={'x': 0.25, 'y': 0.29},
                                   size_hint=(0.25, 0.25), font_size='16sp', color=[.92, 0, .06, 1])

        # ref=link ссылка, markup говорит что теги надо читать, on_ref_press=указываем def
        self.textLogin2 = Label(text="[ref=link]Нет аккаунта? Регистрация[/ref]", pos_hint={'x': 0.4, 'y': 0},
                                size_hint=(0.25, 0.25), font_size='18sp', color=[.92, 0, .06, 1],
                                on_ref_press=self.registration, markup=True)

        # Моя музыка виджеты
        self.textmenu = Label(text="Моя музыка", pos_hint={'x': 0, 'y': 0.75}, size_hint=(0.4, 0.4),
                              font_size='18sp', color=[.92, 0, .06, 1])

        self.lblmain1 = Label(text="   Моя\nмузыка", pos_hint={'x': 0.365, 'y': -0.04}, size_hint=(0.25, 0.25),
                              font_size='12sp', color=[.92, 0, .06, 1])

        self.lblmain2 = Label(text="Плейлисты", pos_hint={'x': 0.18, 'y': -0.04}, size_hint=(0.25, 0.25),
                              font_size='12sp', color=[.92, 0, .06, 1])

        self.lblmain3 = Label(text="Рекомендаций", pos_hint={'x': 0.545, 'y': -0.04}, size_hint=(0.25, 0.25),
                              font_size='12sp', color=[.92, 0, .06, 1])

        self.lblmain4 = Label(text="Настройки", pos_hint={'x': 0.755, 'y': -0.04}, size_hint=(0.25, 0.25),
                              font_size='12sp', color=[.92, 0, .06, 1])

        self.lblmain5 = Label(text="Поиск", pos_hint={'x': -0.01, 'y': -0.04}, size_hint=(0.25, 0.25),
                              font_size='12sp', color=[.92, 0, .06, 1])

        self.btnRec = Button(text="", size_hint=(0.15, 0.15), pos_hint={'x': 0.595, 'y': 0.125},
                             background_normal='image/rec.png', border=(0, 0, 0, 0),
                             background_down='image/rec.png', on_press=self.Rec)

        self.btnPlaylist = Button(text="", size_hint=(0.15, 0.15), pos_hint={'x': 0.255, 'y': 0.125},
                                 background_normal='image/playlist.png', border=(0, 0, 0, 0),
                                 background_down='image/playlist.png',
                                 on_press=self.playlist)

        self.btnsearch = Button(text="", size_hint=(0.15, 0.15), pos_hint={'x': 0.045, 'y': 0.125},
                                background_normal='image/search.png', border=(0, 0, 0, 0),
                                background_down='image/search.png', on_press=self.search)

        # Border нужен чтобы иконка полностью прорисовывалась, down чтобы не было цвета при нажатиях
        self.btnsetting = Button(size_hint=(0.15, 0.15), pos_hint={'x': 0.805, 'y': 0.125},
                                 background_normal='image/settings.png', border=(0, 0, 0, 0),
                                 background_down='image/settings.png', on_press=self.settings)

        self.btnmusic = Button(text="", size_hint=(0.15, 0.15), pos_hint={'x': 0.420, 'y': 0.125},
                               background_normal='image/music.png', border=(0, 0, 0, 0),
                               background_down='image/music.png',
                               on_press=self.Mysound)

        self.btnmain1 = Button(text="Pause", pos_hint={'x': 0.665, 'y': 0.9}, size_hint=(0.15, 0.15),
                              font_size='12sp', color=[.92, 0, .06, 1], on_press=self.pause)

        self.BtnNext =  Button(text="Next", pos_hint={'x': 0.865, 'y': 0.9}, size_hint=(0.15, 0.15),
                              font_size='12sp', color=[.92, 0, .06, 1], on_press=self.nextTrack)

        self.BtnVolume = Button(text="Принять", pos_hint={'x': 0.465, 'y': 0.9}, size_hint=(0.15, 0.15),
                              font_size='12sp', color=[.92, 0, .06, 1], on_press=self.Volume)
        # multiline ограничение строк в одну
        self.txtVolume = TextInput(text="100", size_hint=(0.09, 0.075), pos_hint={'x': 0.365, 'y': 0.9}, multiline=False)

        # Виджеты Регистраций
        self.inputreg1 = TextInput(text="Логин", size_hint=(0.7, 0.08), pos_hint={'x': 0.15, 'y': 0.7})

        self.inputreg2 = TextInput(text="Пароль", size_hint=(0.7, 0.08), pos_hint={'x': 0.15, 'y': 0.5})

        self.inputreg3 = TextInput(text="Телефон", size_hint=(0.7, 0.08), pos_hint={'x': 0.15, 'y': 0.3})

        self.btnReg = Button(text="Регистрация", size_hint=(0.45, 0.1), pos_hint={'x': 0.275, 'y': 0.15},
                             on_press=self.registAutorizat, color=[196, 196, 196, 1])

        self.textReg1 = Label(text="Регистрация", pos_hint={'x': 0.35, 'y': 0.8}, size_hint=(0.25, 0.25),
                               font_size='30sp', color=[.92, 0, .06, 1])

        self.textReg2 = Label(text="Регистрация прошла успешно!", pos_hint={'x': 0.38, 'y': 0}, size_hint=(0.25, 0.25),
                              font_size='14sp', color=[.92, 0, .06, 1])

        # Виджеты меню настроек
        self.textsettings1 = Label(text="Настройки", pos_hint={'x': 0, 'y': 0.8}, size_hint=(0.25, 0.25),
                               font_size='16sp', color=[.92, 0, .06, 1])

        self.dropdown_language = DropDown()
        self.dropdown_language.container.spacing = 2
        self.btnTranslite = Button(text="RUS", on_press=self.dropdown_language.open, size_hint=(0.2, 0.095),
                           pos_hint={'x': 0.1, 'y': 0.8}, color=[196, 196, 196, 1])

        self.dropbtn = Button(text="RUS", size_hint_y=None, height=20, on_press=self.languageRus,
                              color=[196, 196, 196, 1])
        self.dropbtn2 = Button(text="ENG", size_hint_y=None, height=15, on_press=self.languageEng,
                               color=[196, 196, 196, 1])

        self.textsettings1 = Label(text="Язык приложения", pos_hint={'x': 0.45, 'y': 0.725}, size_hint=(0.25, 0.25),
                               font_size='16sp', color=[.92, 0, .06, 1])

        self.dropdown_Theme = DropDown()
        self.dropdown_Theme.container.spacing = 2
        self.btnTheme = Button(text="White", on_press=self.dropdown_Theme.open, size_hint=(0.2, 0.095),
                                   pos_hint={'x': 0.1, 'y': 0.65}, color=[196, 196, 196, 1])

        self.dropbtn3 = Button(text="White", size_hint_y=None, height=25, on_press=self.WhiteTheme,
                               color=[196, 196, 196, 1])
        self.dropbtn4 = Button(text="Dark", size_hint_y=None, height=15, on_press=self.darkTheme,
                               color=[196, 196, 196, 1])

        self.textsettings2 = Label(text="Темная/Светлая тема", pos_hint={'x': 0.45, 'y': 0.575}, size_hint=(0.25, 0.25),
                               font_size='16sp', color=[.92, 0, .06, 1])

        self.textsettings3 = Label(text="Закачивать последнее\nпрослушиваемое аудио", pos_hint={'x': 0.45, 'y': 0.455},
                                   size_hint=(0.25, 0.25), font_size='16sp', color=[.92, 0, .06, 1])

        self.textsettings4 = Label(text="     Стиль уведомлений\nСистемные/Приложения", pos_hint={'x': 0.45, 'y': 0.3},
                                   size_hint=(0.25, 0.25), font_size='16sp', color=[.92, 0, .06, 1])

        self.btnquit = Button(text="Выйти из аккаунта", pos_hint={'x': 0.7, 'y': 0.9}, size_hint=(0.3, 0.1),
                              on_press=self.quitlog, font_size='12sp', color=[196, 196, 196, 1])

        # Виджеты Плейлист
        self.lblPlaylist = Label(text="Плейлисты", pos_hint={'x': 0, 'y': 0.75}, size_hint=(0.4, 0.4),
                              font_size='18sp', color=[.92, 0, .06, 1])

        self.btnPlaylist1 = Button(text="", size_hint=(0.2, 0.2), pos_hint={'x': 0.05, 'y': 0.68},
                                   background_normal='image/playlist1.png', border=(0, 0, 0, 0),
                                   background_down='image/playlist1.png'
                                   )

        self.btnPlaylist2 = Button(text="", size_hint=(0.2, 0.2), pos_hint={'x': 0.3, 'y': 0.68},
                                   background_normal='image/playlist2.png', border=(0, 0, 0, 0),
                                   background_down='image/playlist2.png'
                                   )

        self.btnPlaylist3 = Button(text="", size_hint=(0.2, 0.2), pos_hint={'x': 0.55, 'y': 0.68},
                                   background_normal='image/playlist6.png', border=(0, 0, 0, 0),
                                   background_down='image/playlist6.png'
                                   )

        self.lblPlaylist2 = Label(text="Мой плейлисты", pos_hint={'x': 0.045, 'y': 0.38}, font_size='18sp',
                                  color=[.92, 0, .06, 1], size_hint=(0.4, 0.4))

        self.btnPlaylist4 = Button(text="", size_hint=(0.2, 0.2), pos_hint={'x': 0.05, 'y': 0.3},
                                   background_normal='image/playlist3.png', border=(0, 0, 0, 0),
                                   background_down='image/playlist3.png'
                                   )

        self.btnPlaylist5 = Button(text="", size_hint=(0.2, 0.2), pos_hint={'x': 0.3, 'y': 0.3},
                                   background_normal='image/playlist4.png', border=(0, 0, 0, 0),
                                   background_down='image/playlist4.png', on_press=self.dialog)

        self.musicplaylist = RV()
        self.musicplaylist.data = [{'text': value, 'size_hint_y': None,
                                 'on_press': self.test1, 'background_normal': '',
                                 'height': 25,
                                 'background_color': (0, 0.41, 0.88, 1), 'font_size': '14sp',
                                 'halign': 'center'} for value in os.listdir('track')]

        self.btnAdd = Button(text="Добавить аудиозапись", size_hint=(0.45, 0.1), pos_hint={'x': 0, 'y': 0.1},
                             font_size='12sp')

        self.btnremove = Button(text="Удалить аудиозапись", size_hint=(0.5, 0.1), pos_hint={'x': 0.5, 'y': 0.1},
                             font_size='12sp')

        # Добавление виджетов в Popup Плейлист
        for element in [self.btnAdd, self.musicplaylist, self.btnremove]:
            self.PopupWindow.add_widget(element)

        self.dialog_popup2 = Popup(title='Плейлист', size_hint=(None, None), size=(350, 350), content=self.PopupWindow)

        # Виджеты Пойск
        self.txtSearch1 = TextInput(text="Search", size_hint=(1, 0.08), pos_hint={'x': 0, 'y': 0.925})

        self.btnSearch = Button(text="Наити", pos_hint={'x': 0, 'y': 0.8}, size_hint=(0.25, 0.1), on_press=self.Search)

        # Виджеты Рекомендаций
        self.txtRec = Label(text="Рекомендаций", pos_hint={'x': 0, 'y': 0.75}, size_hint=(0.4, 0.4),
                              font_size='18sp', color=[.92, 0, .06, 1])

        # Добавление виджетов на окно логин
        for element in [self.inputLogin, self.textLogin, self.inputLogin2, self.btnLogin, self.textLogin2,
                        self.checklog1, self.lblreg1]:
            self.fl.add_widget(element)
        return self.fl

    # Авторизация в приложение, вход в приложение
    def autorization(self, instance):
        #if self.inputLogin.text == "admin" and self.inputLogin2.text == "admin":

        # haling Текст по центру кнопки
        # for value in os.listdir(Список треков)
        self.musicspace = RV()
        self.musicspace.data = [{'text': value, 'size_hint_y': None,
                                 'on_press': self.test1, 'background_normal': '',
                                 'height': 50,
                                 'background_color': (0.6, 0.6, 0.6, 1), 'font_size': '12sp',
                                 'halign': 'center'} for value in os.listdir('track')]

        self.fl.clear_widgets()
        # Добавление виджетов в меню музыка
        for element in [self.textmenu, self.btnPlaylist, self.btnRec, self.btnsetting, self.btnsearch, self.musicspace,
                        self.lblmain1, self.lblmain2, self.lblmain3, self.lblmain4, self.lblmain5, self.fakemusic, self.btnmain1,
                        self.BtnNext, self.BtnVolume, self.txtVolume]:
            self.fl.add_widget(element)

        #self.fl.add_widget(self.main_recycleview)
        #else:
        #    txtOpen = Label(text="Неверный логин или пароль", pos_hint={'x': 0.4, 'y': 0.2}, size_hint=(0.25, 0.25),
        #                       font_size='18sp', color=[.92, 0, .06, 1])
        #    self.fl.add_widget(txtOpen)

    # Добавление виджетов Регистрация
    def registration(self, *args):
        self.fl.clear_widgets()
        for element in [self.inputreg1, self.inputreg2, self.inputreg3, self.btnReg, self.textReg1]:
            self.fl.add_widget(element)

    # Подтверждение Регистраций
    def registAutorizat(self, isntance):
        self.fl.add_widget(self.textReg2)
        self.elements()

    # Добавление элементов нужно для окна Регистрация
    def elements(self, *args):
        self.fl.clear_widgets()
        # Виджеты меню логин
        for element in [self.inputLogin, self.textLogin, self.inputLogin2, self.btnLogin, self.textLogin2, self.checklog1,
                        self.lblreg1]:
            self.fl.add_widget(element)

    # Добавление элементов на экран Настройки
    def settings(self, instance):
        self.fl.clear_widgets()
        self.dropdown_Theme.clear_widgets()
        self.dropdown_language.clear_widgets()
        self.dropdown_language.add_widget(self.dropbtn)
        self.dropdown_language.add_widget(self.dropbtn2)
        self.dropdown_Theme.add_widget(self.dropbtn3)
        self.dropdown_Theme.add_widget(self.dropbtn4)
        # Добавление виджетов в меню Настройки
        for element in [self.textsettings1, self.btnTranslite, self.btnTheme, self.textsettings2,
                        self.textsettings3, self.textsettings4, self.btnsearch, self.btnRec, self.btnPlaylist,
                        self.btnmusic, self.btnquit, self.lblmain1, self.lblmain2, self.lblmain3, self.lblmain4,
                        self.lblmain5, self.fakesetting]:
            self.fl.add_widget(element)

    # Виджеты окна Моя музыка
    def Mysound(self, instance):
        self.fl.clear_widgets()
        for element in [self.textmenu, self.btnPlaylist, self.btnRec, self.btnsetting, self.btnsearch, self.musicspace,
                        self.lblmain1, self.lblmain2, self.lblmain3, self.lblmain4, self.lblmain5, self.fakemusic, self.btnmain1,
                        self.BtnNext, self.BtnVolume, self.txtVolume]:
            self.fl.add_widget(element)

    # Возращение в логин
    def quitlog(self, instance):
        self.fl.clear_widgets()
        for element in [self.inputLogin, self.textLogin, self.inputLogin2, self.btnLogin, self.textLogin2,
                        self.checklog1, self.lblreg1]:
            self.fl.add_widget(element)

    # Добавление виджетов в Плейлист
    def playlist(self, instance):
        self.fl.clear_widgets()

        for element in [self.btnRec, self.btnsetting, self.btnsearch, self.btnmusic, self.lblPlaylist, self.btnPlaylist1,
                        self.btnPlaylist2, self.btnPlaylist3, self.lblPlaylist2, self.btnPlaylist4, self.btnPlaylist5,
                        self.lblmain1, self.lblmain2, self.lblmain3, self.lblmain4, self.lblmain5, self.fakePlaylist]:
            self.fl.add_widget(element)

    # Добавление виджетов в Поиск
    def search(self, isntance):
        self.fl.clear_widgets()

        for element in [self.btnRec, self.btnsetting, self.btnmusic, self.btnPlaylist, self.txtSearch1, self.lblmain1,
                        self.lblmain2, self.lblmain3, self.lblmain4, self.lblmain5, self.fakesearch, self.btnSearch]:
            self.fl.add_widget(element)

    # Добавление виджетов в Рекомендации
    def Rec(self, instance):
        self.fl.clear_widgets()

        for element in [self.fakeRec, self.btnsetting, self.btnmusic, self.btnPlaylist, self.txtRec, self.btnsearch,
                        self.lblmain1, self.lblmain2, self.lblmain3, self.lblmain4, self.lblmain5, self.musicspace]:
            self.fl.add_widget(element)

    # Установка громкости музыки
    def Volume(self, instance):
        self.volume1 = self.txtVolume.text
        self.volume2 = (int(self.volume1) / 100)
        print(self.volume2)
        mixer.music.set_volume(self.volume2)

    # Старт воспроизведения музыки
    def test1(self):
        self.music_file = r"C:\Users\vladi\PycharmProjects\music\track\\" + self.selected_music
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
            mixer.music.play()

    def Search(self, instance):
        self.result = self.txtSearch1.text
        pass

    # Воспроизведение музыки через кнопку
    def play(self, instance):
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
            mixer.music.play()

    def nextTrack(self, instance):
        pass

    def backTrack(self, instance):
        pass

    # Поставить паузу музыке
    def pause(self, instance):
        if not self.playing_state:
            mixer.music.pause()
            self.playing_state = True
        else:
            mixer.music.unpause()
            self.playing_state = False

    # Открытие Popup
    def dialog(self, instance):
        self.dialog_popup2.open()

    # Перевод языка на русский язык
    def languageRus(self, instance):
        self.btnTranslite.text = "RUS"

    # Перевод языка на англиский язык
    def languageEng(self, instance):
        self.btnTranslite.text = "ENG"

    # Темная тема приложения
    def darkTheme(self, instance):
        self.btnTheme.text = "Dark"
        Window.clearcolor = (0.15, 0.15, 0.15, 1)

    # Светлая тема приложения
    def WhiteTheme(self, instance):
        self.btnTheme.text = "White"
        Window.clearcolor = (0.66, 0.66, 0.66, 1)


if __name__=='__main__':
    Music().run()
