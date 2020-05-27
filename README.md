# BowserAPI & Tests
Небольшой API на Flask + набор коллекций для Postman + набор тестов на PyTest, созданные для учебных целей

Создано для вебинаров:
- QARATE #5: https://youtu.be/q9Xoic_14M0
- QARATE #6: https://youtu.be/WVNVeHtmBjc

Проект QARATE: https://bit.ly/qarate-public

## Требования
- Postman
- Python 3.x

## Запуск API
### Установка пакетов
1. Перейти в папку с BowserAPI
2. Выполнить
```
pip install -r requirements.txt
```
### Запуск Flask
1. Перейти в папку с BowserAPI
2. Выполнить
```
set FLASK_APP=bowserapi.py
flask run
```
API доступно по адресу http://127.0.0.1:5000/.

Swagger доступен на http://127.0.0.1:5000/apidocs/

## Postman
### Установка окружения
1. Открыть Postman
2. Открыть диалог "Manage environments"
3. Нажать кнопку "Import"
4. Выбрать файл окружения

### Установка коллекций
1. Открыть Postman
2. Ctrl+O
3. В появившемся окне выбрать файл или папку

### Запуск тестов
Смотреть в вебинаре

## PyTest
### Установка пакетов
1. Перейти в папку с PyTest tests
2. Выполнить
```
pip install -r requirements.txt
```

### Запуск тестов
1. В папке "Pytest tests" выполнить
```
pytest
```
Подробнее смотреть в вебинаре