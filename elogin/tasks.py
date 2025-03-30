from elogin.models import Users  # Modelsdan Users ni import qilish
import threading
import requests
from django.apps import apps
from time import sleep

LOGIN_URL = "https://login.emaktab.uz/login"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}

def auto_login_users():
    Users = apps.get_model('elogin', 'Users')  # Modelni kechiktirib yuklash
    users = Users.objects.values_list("login", "password", named=True)

    for user in users:
        session = requests.Session()
        data = {"login": user.login, "password": user.password}
        
        response = session.post(LOGIN_URL, data=data, headers=HEADERS)
        
        if "userfeed" in response.url:
            print(f"✅ {user.login} uchun muvaffaqiyatli login qilindi!")
        else:
            print(f"❌ {user.login} uchun login amalga oshmadi!")

def start_auto_login():
    """Doimiy ishlovchi fon jarayoni."""
    while True:
        auto_login_users()
        sleep(6)  # Har 6 soniyada tekshirib boradi
