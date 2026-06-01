from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from api_client import APIClient

client = APIClient()

class LoginScreen(Screen):
    def do_login(self, username, password):
        self.ids.error_label.text = "Authenticating..."
        res = client.login(username, password)
        if res.get("success"):
            self.manager.current = 'dashboard'
            self.manager.get_screen('dashboard').load_dashboard_data()
        else:
            self.ids.error_label.text = res.get("error", "Login failed")

class DashboardScreen(Screen):
    def load_dashboard_data(self):
        self.ids.data_container.clear_widgets()
        res = client.fetch_data()
        if res.get("success"):
            items = res.get("data", [])
            if not items:
                self.ids.data_container.add_widget(Label(text="No data entries found in Postgres.", size_hint_y=None, height=40))
            for item in items:
                display_text = f"📦 {item.get('name')} - {item.get('description', '')}"
                lbl = Label(text=display_text, size_hint_y=None, height=40, halign='left', valign='middle')
                lbl.bind(size=lbl.setter('text_size'))
                self.ids.data_container.add_widget(lbl)
        else:
            self.ids.data_container.add_widget(Label(text=res.get("error", "Error pulling data"), color=[1,0,0,1]))

class MyMobileApp(App):
    def build(self):
        Builder.load_file('kivy/main.kv')
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm

if __name__ == '__main__':
    MyMobileApp().run()
