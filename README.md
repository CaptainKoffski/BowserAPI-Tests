# BowserAPI & Tests
Небольшой API на Flask + набор коллекций для Postman + набор тестов на PyTest, созданные для учебных целей

Создано для вебинаров:
- QARATE #5: https://youtu.be/q9Xoic_14M0
- QARATE #6: https://youtu.be/WVNVeHtmBjc

Проект QARATE: https://bit.ly/qarate-public

## Требования
- Postman
- Python 3.9+ (рекомендуется последняя версия)
- uv (современный менеджер пакетов Python)

## Быстрая установка

### 1. Установка Python (если не установлен)
**Windows:**
1. Скачать Python с https://www.python.org/downloads/
2. Запустить установщик, обязательно отметить "Add Python to PATH"

**macOS:**
```bash
# С помощью Homebrew (рекомендуется)
brew install python

# Или скачать с https://www.python.org/downloads/
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2. Установка uv (менеджера пакетов)
**Все операционные системы:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Или для Windows PowerShell:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

После установки перезапустите терминал или выполните:
```bash
source ~/.bashrc  # Linux/macOS
# или просто закройте и откройте терминал заново
```

## Запуск API

### Установка зависимостей проекта
1. Открыть терминал/командную строку
2. Перейти в папку проекта:
```bash
cd path/to/BowserAPI-Tests
```
3. Установить все зависимости одной командой:
```bash
uv sync
```

### Запуск Flask API
1. В папке проекта выполнить:
```bash
uv run python BowserAPI/bowserapi.py
```

**Альтернативный способ (через Flask CLI):**
```bash
# Установить переменную окружения
export FLASK_APP=BowserAPI/bowserapi.py  # Linux/macOS
# или для Windows:
# set FLASK_APP=BowserAPI/bowserapi.py

# Запустить
uv run flask run
```

API доступно по адресу http://127.0.0.1:5000/

Swagger доступен на http://127.0.0.1:5000/apidocs/

## Postman
### Установка окружения
1. Открыть Postman
2. Открыть диалог "Manage environments"
3. Нажать кнопку "Import"
4. Выбрать файл `Postman tests/Collections/QARATE Localhost.postman_environment.json`

### Установка коллекций
1. Открыть Postman
2. Ctrl+O (или File → Import)
3. В появившемся окне выбрать папку `Postman tests/Collections/`
4. Импортировать все файлы `.postman_collection.json`

### Запуск тестов
Смотреть в [вебинаре](https://youtu.be/q9Xoic_14M0)

## PyTest

### Запуск тестов
1. В корневой папке проекта выполнить:
```bash
uv run pytest "PyTest tests/"
```

**Для запуска конкретного теста:**
```bash
uv run pytest "PyTest tests/lesson_1_no_pytest/test_no_pytest.py"
```

**Для запуска с подробным выводом:**
```bash
uv run pytest "PyTest tests/" -v
```

Подробнее смотреть в [вебинаре](https://youtu.be/WVNVeHtmBjc)

## Полезные команды uv

```bash
# Добавить новый пакет в проект
uv add package-name

# Удалить пакет
uv remove package-name

# Обновить зависимости
uv sync

# Запуск Python скрипта в виртуальном окружении
uv run python script.py

# Активация виртуального окружения (опционально)
source .venv/bin/activate  # Linux/macOS
# или .venv\Scripts\activate  # Windows
```

## Устранение проблем

**Проблема: "uv: command not found"**
- Перезапустите терминал после установки uv
- Убедитесь, что путь `~/.local/bin` добавлен в PATH

**Проблема: "Python not found"**
- Убедитесь, что Python установлен и добавлен в PATH
- Попробуйте команду `python3` вместо `python`

**Проблема с доступом к API:**
- Убедитесь, что Flask запущен и не выдает ошибки
- Проверьте, что порт 5000 не занят другим приложением
