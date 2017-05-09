from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock

from functools import partial

class DurationClock(Label):
    def update(self, index, *args):
        self.text = index

class TimeApp(App):
    def build(self):
        durclock = DurationClock()
        for i in range(10, 0, -1):
            Clock.schedule_once(partial(durclock.update, str(i)), 10-i)
        return durclock

if __name__ == "__main__":
    TimeApp().run()
