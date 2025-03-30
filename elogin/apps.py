from django.apps import AppConfig
import threading

class EloginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'elogin'

    def ready(self):
        """Django yuklangandan keyin ishga tushadi."""
        from .tasks import start_auto_login
        threading.Thread(target=start_auto_login, daemon=True).start()
