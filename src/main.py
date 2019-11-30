# to change kivy default settings we use this module config
from kivy.config import Config

# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', True)

from time import strftime
import json

from kivy.app import App
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.uix.spinner import Spinner
from kivy.uix.settings import Settings
from kivy.uix.colorpicker import ColorPicker
from kivy.utils import get_color_from_hex
from kivy.uix.settings import SettingsWithSidebar
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView

from settingscolorpicker import SettingColorPicker

speechTypes = {
    'Speech' : {
            "Impromptu": { 60 : "min", 90 : "med", 120: "max" },
            "Speech": { 5 * 60 : "min", 6 * 60 : "med", 7 * 60: "max" },
            "Evaluation": { 120 : "min", 150 : "med", 180: "max" }
            },
    'Sprint': {
            "Daily":  { 10 * 60 : "min", 12.5 * 60 : "med", 15 * 60: "max" },
            "Sprint": { 8 * 60 : "min", 9 * 60 : "med", 10 * 60: "max" },
            "Demo": { 30 * 60 : "min", 35 * 60 : "med", 40 * 60: "max" }
            },
    'Test': {
            "Test": { 2 : "min", 3 : "med", 4: "max" }
            }
        }

intervals = (
    ('w', 604800),  # 60 * 60 * 24 * 7
    ('d', 86400),    # 60 * 60 * 24
    ('h', 3600),    # 60 * 60
    ('m', 60),
    ('s', 1),
    )

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{}{}".format(value, name))
    return ', '.join(result[:granularity])


class RootWidget(BoxLayout):
    pass


class SettingsClass(SettingsWithSidebar):
    pass


class sessionResults(BoxLayout):
    pass


class ConfirmPopup(Popup):
    text = StringProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super(ConfirmPopup, self).__init__(**kwargs)

    def on_answer(self, *args):
        pass


class toastmastersclockApp(App):
    sw_started = BooleanProperty(False)
    sw_seconds = 0
    background = ListProperty()
    categoryValues = ListProperty()
    defaultSpeechName = '< Select >'
    speechNameValues = ListProperty([defaultSpeechName])
    sessTimes = ListProperty([])
    sessLastResult = BooleanProperty(False)
    popupWindow = None

    def update_time(self, nap):
        if self.sw_started:
            self.sw_seconds += nap
            self._check_elapsed_time()
        minutes, seconds = divmod(self.sw_seconds, 60)
        self.root.ids.stopwatch.text = (
            '[b]%02d:%02d.[size=40]%02d[/size][/b]' %
            (int(minutes), int(seconds),
             int(seconds * 100 % 100))
        )
        self.root.ids.time.text = strftime('%H:%M:%S')

    def _get_config_colors(self):
        '''Gets the colors configured in the settings'''
        return {color: self.config.get('screen_colors', color) for color in self._default_colors()}

    def _check_elapsed_time(self):
        """Checks the elapsed time and changes the backgroun accordingly"""
        colors = self._get_config_colors()
        category_string = self.root.ids.category.text
        speech_string = self.speech_string()
        if category_string in speechTypes.keys() and speech_string in speechTypes[category_string].keys():
            selectedCategory = speechTypes[category_string][speech_string]
            for seconds in selectedCategory:
                if int(self.sw_seconds) == seconds:
                    self.background = get_color_from_hex(colors[selectedCategory[seconds]])

    def on_start(self):
        Clock.schedule_interval(self.update_time, 0)

    def start_stop(self):
        self.root.ids.start_stop.text = (
            'Start' if self.sw_started else 'Stop'
        )
        self.sw_started = not self.sw_started

    def speech_string(self):
        return self.root.ids.speechName.text.split(':')[0].strip()

    def get_time_str_resized(self):
        return self.root.ids.stopwatch.text.replace('[size=40]','[size=30]')

    def get_session_tuple(self):
        return (self.speech_string(), self.get_time_str_resized(), self.background)

    def reset(self):
        if self.sw_started:
            self.root.ids.start_stop.text = 'Start'
            self.sw_started = False
        if self.sw_seconds > 0:
            add_tup = self.get_session_tuple()
            if self.sessLastResult:
                self.sessTimes[-1] = add_tup
                self.sessLastResult = False
            else:
                self.sessTimes.append(add_tup)
        self.sw_seconds = 0
        self.background = get_color_from_hex(self._get_config_colors()['default'])

    def category_changed(self, category_name):
        labels = []
        if category_name in speechTypes.keys():
            speeches = sorted(speechTypes[category_name])
            for speechName in speeches:
                minval = display_time(min(speechTypes[category_name][speechName]))
                maxval = display_time(max(speechTypes[category_name][speechName]))
                labels.append('{} : {} - {}'.format(speechName, minval, maxval))
            self.speechNameValues = labels
            self.root.ids.speechName.text = self.defaultSpeechName

    def build(self):
        self.icon = 'assets/icon.png'
        self.settings_cls = SettingsWithSidebar
        root = RootWidget()
        self.categoryValues = sorted(speechTypes.keys())
        self.reset()
        return root

    def build_config(self, config):
        config.setdefaults('screen_colors', self._default_colors())

    def build_settings(self, settings):
        settings.register_type('colorpicker', SettingColorPicker)
        menu_colors = []
        for color in sorted(self._default_colors().keys()):
            menu_colors.append({'type': 'colorpicker',
                                'title': '{} color'.format(color),
                                'desc': '{} color background'.format(color),
                                'section': 'screen_colors',
                                'key': color})
        settings.add_json_panel('display colors',
                                self.config,
                                data=json.dumps(menu_colors))

    def do_quit(self, *largs):
        # print('App quit')
        if platform == 'android':
            self.root_window.close()  # Fix app exit on Android.
        return super(toastmastersclockApp, self).stop(*largs)

    def _default_colors(self):
        ''' Definies the default colors for the application '''
        return { "min": '#00FF00', "med": '#FFFF00', "max": '#FF0000', 'default': '#000000' }

    def session_reset(self):
        content = ConfirmPopup(text='Are you sure you want to reset session values?', title='reset session')
        content.bind(on_answer=self._on_answer)
        self.popup = content
        self.popup.open()

    def _on_answer(self, instance, answer):
        self.popup.dismiss()
        if answer:
            self.sessTimes = []

    def session_show(self):
        tup = self.get_session_tuple()
        if not self.sw_started and self.sw_seconds > 0 and self.sessTimes[-1] != tup:
            if self.sessLastResult:
                self.sessTimes[-1] = tup
            else:
                self.sessTimes.append(tup)
            self.sessLastResult = True
        show = sessionResults()
        oldcat = ''
        data = []
        for msg in self.sessTimes:
            if oldcat != msg[0]:
                n = 0
                oldcat = msg[0]
                data.append(('[b]{}[/b]'.format(msg[0]),(1,1,1,1)))
            n += 1
            data.append(('{}: {}'.format(n, msg[1]), msg[2]))
        show.ids['session_rv'].data = [{'text': x[0], 'background_color': x[1]} for x in data]
        self.popupWindow = Popup(title="Session results", content=show, size_hint=(None, None), size=Window.size)
        self.popupWindow.open()

    def close_results(self):
        self.popupWindow.dismiss()


if __name__ == '__main__':
    toastmastersclockApp().run()
