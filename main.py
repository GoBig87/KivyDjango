import subprocess
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'

from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.clock import Clock   
from kivymd.app import MDApp
from jnius import autoclass
from android.runnable import run_on_ui_thread

WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.kivy.android.PythonActivity').mActivity

Builder.load_string("""
<HomeScreen>
    BoxLayout:
        orientation: "vertical"
        Button:
            id: status_box
            size_hint_x: 0.7
            text: "Hello world"
    AnchorLayout:
        anchor_x: "right"
        anchor_y: "bottom"
        padding: dp(20), dp(20)
        MDFillRoundFlatButton:
            text: "hello world"
""")


class KivyDjango(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Teal"

    def build(self):
        subprocess.call(['python', './backend/manage.py', 'runserver'])
        self.mainbox = FloatLayout()
        self.screens = AnchorLayout(anchor_x='center', anchor_y='center')

        self.content = ScreenManager()
        self.content.transition = NoTransition()
        self.content.add_widget(HomeScreen(name="home"))
        self.screens.add_widget(self.content)
        self.mainbox.add_widget(self.screens)
        Clock.schedule_once(self.create_webview, 0)
        return self.mainbox

    @run_on_ui_thread
    def create_webview(self, *args):
        webview = WebView(activity)
        webview.getSettings().setJavaScriptEnabled(True)
        wvc = WebViewClient();
        webview.setWebViewClient(wvc);
        activity.setContentView(webview)
        webview.loadUrl('http://127.0.0.1:8000/')


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)


KivyDjango().run()