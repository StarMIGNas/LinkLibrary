# 🔖 LinkLibrary — Локальная зашифрованная библиотека ссылок | Local Encrypted Bookmark Manager | مكتبة الروابط المشفرة

![Python](https://shields.io)
![FastHTML](https://shields.io)
![Platform](https://shields.io)
![Encryption](https://shields.io)

**Языки / Languages / اللغات:** [🇷🇺 Русский](#-русский) | [🇬🇧 English](#-english) | [🇸🇦 العربية](#-العربية)

---

## 🇷🇺 Русский

**LinkLibrary** — это легкое десктопное приложение для Windows для хранения полезных интернет-ссылок с описаниями. Все данные хранятся локально на вашем компьютере в зашифрованном файле и защищены мастер-паролем.

### ✨ Основные возможности
* **🔐 Защита мастер-паролем**: При первом запуске создается пароль, на основе которого генерируется ключ шифрования. Без пароля прочитать базу ссылок невозможно.
* **🛡️ Локальное шифрование**: Все закладки сохраняются в файл `links.enc` с использованием симметричного шифрования `Fernet` (AES). Никаких облаков и сторонних серверов.
* **🔍 Мгновенный живой поиск**: Фильтрация карточек по описанию или адресу сайта в реальном времени без перезагрузки интерфейса.
* **✏️ Удобное управление**: Добавление ссылок (с автоматической подстановкой `https://`), редактирование описаний, удаление и быстрое открытие сайтов в основном браузере системы.
* **🖥️ Нативное окно Windows**: Приложение работает как самостоятельная десктопная программа благодаря обертке `PyWebView` и может быть собрано в один исполняемый файл `.exe`.

### 🚀 Установка и запуск
```powershell
git clone https://github.com
cd LinkLibrary
python -m venv .venv
.venv\Scripts\activate
pip install python-fasthtml pywebview cryptography uvicorn pyinstaller
python main.py
```

### 📦 Сборка в `.exe` (Windows)
```powershell
pyinstaller --noconsole --onefile --name "LinkLibrary" --collect-all fasthtml main.py
```

### ⚠️ Примечание по безопасности
Приложение предназначено для хранения интернет-закладок, статей и рабочих ссылок. **Не используйте его** для хранения сид-фраз криптокошельков или банковских паролей.

---

## 🇬🇧 English

**LinkLibrary** is a lightweight desktop application for Windows designed to store useful web links with custom descriptions. All data is stored locally on your machine in an encrypted file protected by a master password.

### ✨ Key Features
* **🔐 Master Password Protection**: On the first launch, you set a password used to derive the encryption key. Your bookmarks cannot be read without it.
* **🛡️ Local Encryption**: All links are saved in a local `links.enc` file using `Fernet` (AES) symmetric encryption. No cloud storage or third-party servers.
* **🔍 Instant Live Search**: Filter cards by description or website URL in real time without reloading the interface.
* **✏️ Easy Management**: Add links (with automatic `https://` prefixing), edit descriptions, delete items, and open websites directly in your default system browser.
* **🖥️ Native Windows Window**: Runs as a standalone desktop app powered by `PyWebView` and can be packaged into a single `.exe` executable.

### 🚀 Installation & Run
```powershell
git clone https://github.com
cd LinkLibrary
python -m venv .venv
.venv\Scripts\activate
pip install python-fasthtml pywebview cryptography uvicorn pyinstaller
python main.py
```

### 📦 Build `.exe` (Windows)
```powershell
pyinstaller --noconsole --onefile --name "LinkLibrary" --collect-all fasthtml main.py
```

### ⚠️ Security Disclaimer
This application is intended for storing web bookmarks, articles, and everyday links. **Do not use it** to store cryptocurrency wallet seed phrases or critical banking passwords.

---

## 🇸🇦 العربية

<div dir="rtl">

**LinkLibrary** هو تطبيق سطح مكتب خفيف لنظام التشغيل Windows مصمم لحفظ روابط الإنترنت المفيدة مع إضافة وصف لكل رابط. يتم تخزين جميع البيانات محليًا على جهازك في ملف مشفر ومحمي بكلمة مرور رئيسية.

### ✨ المميزات الرئيسية
* **🔐 الحماية بكلمة مرور رئيسية**: عند التشغيل لأول مرة، تقوم بإنشاء كلمة مرور تُستخدم لتوليد مفتاح التشفير. لا يمكن قراءة قاعدة الروابط بدونها.
* **🛡️ تشفير محلي بالكامل**: يتم حفظ جميع الروابط في ملف `links.enc` باستخدام تشفير `Fernet` (AES) المتماثل. لا توجد خوادم خارجية أو تخزين سحابي.
* **🔍 بحث فوري ومباشر**: تصفية البطاقات حسب الوصف أو عنوان الموقع في الوقت الفعلي دون إعادة تحميل الواجهة.
* **✏️ إدارة سهلة وسريعة**: إضافة الروابط (مع إضافة `https://` تلقائيًا)، تعديل الأوصاف، حذف الروابط، وفتح المواقع مباشرة في متصفحك الافتراضي.
* **🖥️ نافذة Windows مستقلة**: يعمل التطبيق كبرنامج سطح مكتب مستقل بفضل مكتبة `PyWebView` ويمكن تجميعه في ملف تنفيذي واحد بصيغة `.exe`.

### 🚀 التثبيت والتشغيل
</div>

```powershell
git clone https://github.com
cd LinkLibrary
python -m venv .venv
.venv\Scripts\activate
pip install python-fasthtml pywebview cryptography uvicorn pyinstaller
python main.py
```

<div dir="rtl">

### 📦 تجميع البرنامج إلى ملف `.exe` (Windows)
</div>

```powershell
pyinstaller --noconsole --onefile --name "LinkLibrary" --collect-all fasthtml main.py
```

<div dir="rtl">

### ⚠️ تنبيه أمني هام
هذا التطبيق مخصص لحفظ إشارات المواقع المرجعية والمقالات والروابط اليومية. **يُرجى عدم استخدامه** لحفظ عبارات الاسترداد (Seed Phrases) لمحافظ العملات الرقمية أو كلمات المرور البنكية الحساسة.

</div>

---

## 📄 Лицензия / License / الرخصة
MIT License
