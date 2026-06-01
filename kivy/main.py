import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from api_client import APIClient

class LoginDashboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        self.client = APIClient()

        self.status_label = Label(text="Welcome! Please Log In.", size_hint_y=None, height=40)
        self.username_input = TextInput(hint_text="Username", multiline=False, size_hint_y=None, height=40)
        self.password_input = TextInput(hint_text="Password", password=True, multiline=False, size_hint_y=None, height=40)
        
        self.login_btn = Button(text="Login & Fetch Data", size_hint_y=None, height=50)
        self.login_btn.bind(on_press=self.start_login_thread)
        
        self.data_label = Label(text="Cloud Data will appear here...", halign='center', valign='middle')
        self.data_label.bind(size=self.data_label.setter('text_size'))

        self.add_widget(self.status_label)
        self.add_widget(self.username_input)
        self.add_widget(self.password_input)
        self.add_widget(self.login_btn)
        self.add_widget(self.data_label)

    def start_login_thread(self, instance):
        self.status_label.text = "Connecting to Cloud API... Please wait."
        self.login_btn.disabled = True
        threading.Thread(target=self.network_operations, daemon=True).start()

    def network_operations(self):
        user = self.username_input.text
        pwd = self.password_input.text
        
        login_res = self.client.login(user, pwd)
        if not login_res["success"]:
            Clock.schedule_once(lambda dt: self.update_ui_failure(login_res["error"]))
            return

        data_res = self.client.fetch_data()
        if data_res["success"]:
            Clock.schedule_once(lambda dt: self.update_ui_success(data_res["data"]))
        else:
            Clock.schedule_once(lambda dt: self.update_ui_failure(data_res["error"]))

    def update_ui_success(self, data):
        self.status_label.text = "Successfully Connected to Cloud PostgreSQL!"
        self.login_btn.disabled = False
        self.data_label.text = f"Payload from Server:\n{str(data)}"

    def update_ui_failure(self, error_message):
        self.status_label.text = f"Error: {error_message}"
        self.login_btn.disabled = False

class CloudConnectedApp(App):
    def build(self):
        return LoginDashboard()

if __name__ == '__main__':
    CloudConnectedApp().run()