import base64
import hashlib
import json
import os
import sys
import threading
import time
import uuid
import webbrowser
import uvicorn
import webview
from cryptography.fernet import Fernet, InvalidToken
from fasthtml.common import *

# Определяем папку, где лежит сам скрипт или собранный .exe файл
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "links.enc")

# Храним пароль текущей сессии в оперативной памяти
CURRENT_PASSWORD = None

app, rt = fast_app(pico=True)


# --- БЛОК ШИФРОВАНИЯ ---
def make_key(password: str) -> bytes:
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest)


def load_links(password: str):
    if not os.path.exists(DATA_FILE):
        return []
    fernet = Fernet(make_key(password))
    with open(DATA_FILE, "rb") as f:
        encrypted_data = f.read()
    decrypted_bytes = fernet.decrypt(encrypted_data)
    return json.loads(decrypted_bytes.decode("utf-8"))


def save_links(links: list, password: str):
    fernet = Fernet(make_key(password))
    json_bytes = json.dumps(links, ensure_ascii=False).encode("utf-8")
    encrypted_data = fernet.encrypt(json_bytes)
    with open(DATA_FILE, "wb") as f:
        f.write(encrypted_data)


# --- ИНТЕРФЕЙС ВХОДА (ПАРОЛЬ) ---
def render_login(error_msg=""):
    is_new = not os.path.exists(DATA_FILE)
    title_text = "🔐 Создание мастер-пароля" if is_new else "🔐 Вход в библиотеку"
    hint_text = (
        "Придумайте пароль. Им будет зашифрован файл ваших ссылок."
        if is_new
        else "Введите мастер-пароль для расшифровки ваших ссылок."
    )
    btn_text = "Создать и войти" if is_new else "Разблокировать"

    return Title("Вход в библиотеку"), Main(
        Article(
            H2(title_text),
            P(hint_text),
            P(error_msg, style="color: #e74c3c; font-weight: bold;") if error_msg else "",
            Form(
                Input(type="password", name="password", placeholder="Введите пароль...", required=True, autofocus=True),
                Button(btn_text, type="submit"),
                action="/login",
                method="POST",
            ),
            style="max-width: 450px; margin: 60px auto;",
        ),
        cls="container",
    )


# --- ИНТЕРФЕЙС КАРТОЧКИ ССЫЛКИ ---
def render_link_card(item: dict):
    lid = item["id"]
    return Article(
        Div(
            Small(item["url"], style="color: #7f8c8d; word-break: break-all;"),
            H4(item["description"], style="margin: 5px 0 12px 0;"),
            # Скрытая форма редактирования (открывается по клику)
            Details(
                Summary(
                    "✏️ Редактировать описание",
                    role="button",
                    cls="outline secondary",
                    style="padding: 4px 10px; font-size: 14px;",
                ),
                Form(
                    Fieldset(
                        Input(type="text", name="description", value=item["description"], required=True),
                        Button("Сохранить", type="submit"),
                        role="group",
                    ),
                    action=f"/edit/{lid}",
                    method="POST",
                    style="margin-top: 10px;",
                ),
            ),
            Div(
                A("🌐 Открыть в браузере", href=f"/open/{lid}", role="button", style="margin-right: 10px;"),
                A(
                    "✖ Удалить",
                    href=f"/delete/{lid}",
                    role="button",
                    cls="secondary",
                    onclick="return confirm('Удалить эту ссылку?');",
                ),
                style="margin-top: 12px;",
            ),
        ),
        style="margin-bottom: 15px; padding: 15px 20px;",
    )


# --- МАРШРУТЫ (ЛОГИКА ПРИЛОЖЕНИЯ) ---
@rt("/")
def get():
    if not CURRENT_PASSWORD:
        return render_login()

    links = load_links(CURRENT_PASSWORD)
    cards = (
        [render_link_card(item) for item in links]
        if links
        else [P("Пока нет сохраненных ссылок. Добавьте первую выше!")]
    )

    return Title("Моя библиотека ссылок"), Main(
        Div(
            H2("🔖 Моя библиотека сайтов", style="margin: 0;"),
            A("🔒 Заблокировать", href="/logout", role="button", cls="outline contrast"),
            style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;",
        ),
        # Форма добавления новой ссылки
        Article(
            Form(
                Input(type="text", name="url", placeholder="Вставьте ссылку (например: youtube.com)", required=True),
                Input(type="text", name="description", placeholder="Краткое описание: о чем этот сайт?"),
                Button("➕ Сохранить в библиотеку", type="submit"),
                action="/add",
                method="POST",
            )
        ),
        # Строка мгновенного поиска по списку
        Input(
            type="search",
            id="search-box",
            placeholder="🔍 Поиск по описанию или адресу сайта...",
            oninput="filterLinks()",
            style="margin-bottom: 20px;",
        ),
        # Контейнер со всеми сохраненными ссылками
        Div(*cards, id="links-container"),
        # Скрипт для мгновенной фильтрации карточек при вводе текста
        Script("""
            function filterLinks() {
                const query = document.getElementById('search-box').value.toLowerCase();
                const cards = document.querySelectorAll('#links-container article');
                cards.forEach(card => {
                    const text = card.innerText.toLowerCase();
                    card.style.display = text.includes(query) ? '' : 'none';
                });
            }
        """),
        cls="container",
        style="max-width: 850px; padding-top: 20px;",
    )


@rt("/login")
def post(password: str):
    global CURRENT_PASSWORD
    password = password.strip()
    if not password:
        return render_login("Пароль не может быть пустым.")

    # Если файла еще нет — создаем пустую зашифрованную базу с этим паролем
    if not os.path.exists(DATA_FILE):
        save_links([], password)
        CURRENT_PASSWORD = password
        return RedirectResponse("/", status_code=303)

    # Если файл уже есть — пробуем расшифровать
    try:
        load_links(password)
        CURRENT_PASSWORD = password
        return RedirectResponse("/", status_code=303)
    except InvalidToken:
        return render_login("❌ Неверный пароль! Попробуйте еще раз.")


@rt("/logout")
def get():
    global CURRENT_PASSWORD
    CURRENT_PASSWORD = None
    return RedirectResponse("/", status_code=303)


@rt("/add")
def post(url: str, description: str = ""):
    if not CURRENT_PASSWORD:
        return RedirectResponse("/", status_code=303)

    url = url.strip()
    if url and not url.startswith(("http://", "https://")):
        url = "https://" + url

    if url:
        links = load_links(CURRENT_PASSWORD)
        links.insert(
            0,
            {
                "id": str(uuid.uuid4()),
                "url": url,
                "description": description.strip() or "Без описания",
            },
        )
        save_links(links, CURRENT_PASSWORD)

    return RedirectResponse("/", status_code=303)


@rt("/edit/{lid}")
def post(lid: str, description: str):
    if not CURRENT_PASSWORD:
        return RedirectResponse("/", status_code=303)

    links = load_links(CURRENT_PASSWORD)
    for item in links:
        if item["id"] == lid:
            item["description"] = description.strip() or "Без описания"
            break
    save_links(links, CURRENT_PASSWORD)
    return RedirectResponse("/", status_code=303)


@rt("/delete/{lid}")
def get(lid: str):
    if not CURRENT_PASSWORD:
        return RedirectResponse("/", status_code=303)

    links = load_links(CURRENT_PASSWORD)
    links = [item for item in links if item["id"] != lid]
    save_links(links, CURRENT_PASSWORD)
    return RedirectResponse("/", status_code=303)


@rt("/open/{lid}")
def get(lid: str):
    if not CURRENT_PASSWORD:
        return RedirectResponse("/", status_code=303)

    links = load_links(CURRENT_PASSWORD)
    for item in links:
        if item["id"] == lid:
            webbrowser.open(item["url"])
            break
    return RedirectResponse("/", status_code=303)


# --- ЗАПУСК СЕРВЕРА И ОКНА WINDOWS ---
def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="error")


if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(0.5)

    webview.create_window("Моя библиотека ссылок", "http://127.0.0.1:8765", width=920, height=700)
    webview.start()
