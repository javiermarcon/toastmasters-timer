# to change kivy default settings we use this module config
from kivy.config import Config

# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', True)

from time import strftime
from collections import OrderedDict

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.uix.spinner import Spinner

colors = { "green": [0, 1, 0, 1], "yellow": [1, 1, 0, 1], "red": [1, 0, 0, 1] }
categoriesTimes = OrderedDict()
categoriesTimes["Impromptu"] = { 60 : "green", 90 : "yellow", 120: "red" }
categoriesTimes["Speech"] = { 5 * 60 : "green", 6 * 60 : "yellow", 7 * 60: "red" }
categoriesTimes["Sprint"] = { 8 * 60 : "green", 9 * 60 : "yellow", 10 * 60: "red" }
categoriesTimes["Test"] = { 2 : "green", 3 : "yellow", 4: "red" }

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
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

class RootWidget(BoxLayout):
    pass

class toastmastersclockApp(App):
    sw_started = BooleanProperty(False)
    sw_seconds = 0
    background = ListProperty()
    spinnerValues = ListProperty()
    spinnerText = StringProperty()

    def _get_spinner_values(self):
        labels = []
        for category in categoriesTimes.keys():
            minval = display_time(min(categoriesTimes[category]))
            maxval = display_time(max(categoriesTimes[category]))
            labels.append('{} : {} - {}'.format(category, minval, maxval))
        return labels

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
        category_string = self.root.ids.spinner_1.text.split(':')[0].strip()
        selectedCategory = categoriesTimes[category_string]
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

    #def spinnerChanged(self, textValue):
    #    print(textValue)

    def build(self):
        self.icon = 'assets/icon.png'
        root = RootWidget()
        spinner_values = self._get_spinner_values()
        self.spinnerValues = spinner_values
        self.spinnerText = spinner_values[0]
        self.reset()
        return root

if __name__ == '__main__':
    toastmastersclockApp().run()
