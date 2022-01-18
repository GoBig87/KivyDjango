import subprocess
import os
from threading import Thread
from django.core.management import execute_from_command_line
from kivy.app import App

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_web_app.settings'

from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.clock import Clock   
from jnius import autoclass
from android.runnable import run_on_ui_thread

WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.kivy.android.PythonActivity').mActivity

from kivy.utils import platform
if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])


Builder.load_string("""
<HomeScreen>
    BoxLayout:
        Widget:
        BoxLayout:
            orientation: "vertical"
            Widget:
            Label:
                id: status_box
                size_hint_x: 0.7
                text: "Hello world"
            Widget:
        Widget:
""")


@run_on_ui_thread
def create_webview(*args):
    webview = WebView(activity)
    webview.getSettings().setJavaScriptEnabled(True)
    wvc = WebViewClient()
    webview.setWebViewClient(wvc)
    activity.setContentView(webview)
    webview.loadUrl('http://127.0.0.1:8000/')


class KivyDjango(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.run_django_thread()
        self.mainbox = FloatLayout()
        self.screens = AnchorLayout(anchor_x='center', anchor_y='center')

        self.content = ScreenManager()
        self.content.transition = NoTransition()
        self.content.add_widget(HomeScreen(name="home"))
        self.screens.add_widget(self.content)
        self.mainbox.add_widget(self.screens)
        Clock.schedule_once(create_webview, 5)
        return self.mainbox

    def run_django_thread(self):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_web_app.settings')
        thread = Thread(target=execute_from_command_line, args=(["python", "runserver", "--noreload"],))
        thread.start()



class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)


KivyDjango().run()