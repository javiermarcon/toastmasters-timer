# to change kivy default settings we use this module config
from kivy.config import Config

# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', True)

from time import strftime
from collections import OrderedDict

from kivy.app import App
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.uix.spinner import Spinner

colors = { "green": [0, 1, 0, 1], "yellow": [1, 1, 0, 1], "red": [1, 0, 0, 1] }
speechTypes = {
    'Speech' : {
            "Impromptu": { 60 : "green", 90 : "yellow", 120: "red" },
            "Speech": { 5 * 60 : "green", 6 * 60 : "yellow", 7 * 60: "red" },
            "Evaluation": { 120 : "green", 150 : "yellow", 180: "red" }
            },
    'Sprint': {
            "Daily":  { 10 * 60 : "green", 12.5 * 60 : "yellow", 15 * 60: "red" },
            "Sprint": { 8 * 60 : "green", 9 * 60 : "yellow", 10 * 60: "red" },
            "Demo": { 30 * 60 : "green", 35 * 60 : "yellow", 40 * 60: "red" }
            },
    'Test': {
            "Test": { 2 : "green", 3 : "yellow", 4: "red" }
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

class toastmastersclockApp(App):
    sw_started = BooleanProperty(False)
    sw_seconds = 0
    background = ListProperty()
    categoryValues = ListProperty()
    defaultSpeechName = '< Select >'
    speechNameValues = ListProperty([defaultSpeechName])

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

    def _check_elapsed_time(self):
        """Checks the elapsed time and changes the backgroun accordingly"""
        category_string = self.root.ids.category.text
        speech_string = self.root.ids.speechName.text.split(':')[0].strip()
        if category_string in speechTypes.keys() and speech_string in speechTypes[category_string].keys():
            selectedCategory = speechTypes[category_string][speech_string]
            for seconds in selectedCategory:
                if int(self.sw_seconds) == seconds:
                    self.background = colors[selectedCategory[seconds]]

    def on_start(self):
        Clock.schedule_interval(self.update_time, 0)

    def start_stop(self):
        self.root.ids.start_stop.text = (
            'Start' if self.sw_started else 'Stop'
        )
        self.sw_started = not self.sw_started

    def reset(self):
        if self.sw_started:
            self.root.ids.start_stop.text = 'Start'
            self.sw_started = False
        self.sw_seconds = 0
        self.background = [1, 1, 1, 1]

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
        root = RootWidget()
        self.categoryValues = sorted(speechTypes.keys())
        self.reset()
        return root

    def do_quit(self, *largs):
        # print('App quit')
        if platform == 'android':
            self.root_window.close()  # Fix app exit on Android.
        return super(toastmastersclockApp, self).stop(*largs)

if __name__ == '__main__':
    toastmastersclockApp().run()
