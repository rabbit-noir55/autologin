from .models import Users

import openpyxl
def check_user(login):
  return Users.objects.filter(login=login).exists()
def add_user(login,password):
  Users.objects.create(login=login, password=password)

def read_xls_columns(file):
    """ Excel faylidan A va B ustunlarini o‘qish """
    try:
        wb = openpyxl.load_workbook(file, data_only=True)  # Formulalarni natija sifatida o‘qish
        sheet = wb.active
        a_list = [cell.value for cell in sheet['A'] if cell.value is not None]
        b_list = [cell.value for cell in sheet['B'] if cell.value is not None]
        return a_list, b_list
    except openpyxl.utils.exceptions.InvalidFileException:
        return None, None
    except Exception as e:
        print(f"Xatolik: {e}")
        return None, None
import os

def is_excel(file):
    """ Fayl kengaytmasi bo‘yicha Excel fayli ekanligini tekshirish """
    excel_extensions = {".xls", ".xlsx"}
    
    if isinstance(file, str):  # Fayl nomi sifatida kelsa
        ext = os.path.splitext(file)[1].lower()
    else:  # Django yoki Flask file-like object sifatida kelsa
        ext = os.path.splitext(file.name)[1].lower()

    return ext in excel_extensions
def add_user_list(logins, passwords):
    """
    Login va parollarni Users modeliga saqlaydi.
    - Agar login avval mavjud bo‘lsa, uni qo‘shmaydi.
    - Faqat yangi foydalanuvchilar bulk_create orqali saqlanadi.
    
    logins: list - Foydalanuvchi loginlari ro‘yxati
    passwords: list - Foydalanuvchi parollari ro‘yxati
    
    return: Yangi qo‘shilgan foydalanuvchilar soni
    """
    if len(logins) != len(passwords):
        raise ValueError("Logins va Passwords uzunligi bir xil bo‘lishi kerak!")

    # Bazadagi mavjud loginlarni olish
    existing_users = set(Users.objects.values_list("login", flat=True))

    # Yangi foydalanuvchilar ro‘yxatini yaratish
    new_users = [
        Users(login=log, password=pas)
        for log, pas in zip(logins, passwords)
        if log not in existing_users
    ]

    # Agar yangi foydalanuvchilar bo‘lsa, bulk_create orqali saqlaymiz
    if new_users:
        Users.objects.bulk_create(new_users)

    return len(new_users)  # Yangi qo‘shilgan foydalanuvchilar sonini qaytaradi
