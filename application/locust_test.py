from locust import HttpUser, task, between
from bs4 import BeautifulSoup
import random
import string


class AuthUser(HttpUser):
    wait_time = between(1, 3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email = None
        self.password = "Test_password123!"
        self.csrf_token = None

    def get_csrf_token(self, response_text):
        soup = BeautifulSoup(response_text, 'html.parser')
        return soup.find('input', {'name': 'csrf_token'})['value']

    def generate_unique_email(self):
        random_str = ''.join(random.choices(string.ascii_lowercase, k=12))
        return f"locust_{random_str}@example.com"

    def on_start(self):
        self.email = self.generate_unique_email()
        self.register()
        self.login()

    def register(self):
        response = self.client.get("/registration")
        self.csrf_token = self.get_csrf_token(response.text)

        data = {
            "csrf_token": self.csrf_token,
            "email": self.email,
            "name": "Locust",
            "surname": "Test",
            "password": self.password,
            "confirm": self.password,
            "checkbox": "y",
            "patronymic": "User"
        }

        with self.client.post("/registration", data=data, catch_response=True) as response:
            if response.status_code == 302:
                response.success()
            else:
                response.failure(f"Registration failed: {response.text}")

    @task(3)
    def login(self):
        response = self.client.get("/login")
        self.csrf_token = self.get_csrf_token(response.text)

        data = {
            "csrf_token": self.csrf_token,
            "email": self.email,
            "password": self.password,
            "remember": False
        }

        with self.client.post("/login", data=data, catch_response=True) as response:
            if (response.status_code == 200
                    and "Выйти из аккаунта" in response.text
                    and self.email in response.text):
                response.success()
            else:
                response.failure(f"Login failed: {response.text[:200]}")

    @task(1)
    def logout(self):
        response = self.client.get("/logout")
        self.csrf_token = self.get_csrf_token(response.text)

        with self.client.post(
                "/logout",
                data={"csrf_token": self.csrf_token},
                catch_response=True
        ) as response:
            if any(text in response.text for text in ["Войти в аккаунт", "Авторизоваться"]):
                response.success()
                self.client.cookies.clear()
            else:
                response.failure(f"Logout failed. Status: {response.status_code}")