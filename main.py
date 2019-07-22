from time import strftime

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ListProperty

class RootWidget(BoxLayout):
    pass

class toastmastersclockApp(App):
    sw_started = BooleanProperty(False)
    sw_seconds = 0
    background = ListProperty()

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
        colors = {
            5 : [0, 1, 0, 1],
            6 : [1, 1, 0, 1],
            1 * 7: [1, 0, 0, 1],
        }
        for seconds in colors:
            if int(self.sw_seconds) == seconds:
                self.background = colors[seconds]

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

    def build(self):
        root = RootWidget()
        self.reset()
        return root

if __name__ == '__main__':
    toastmastersclockApp().run()
