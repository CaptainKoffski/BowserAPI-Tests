# BowserAPI-PostmanDemo
Небольшой API на Flask + набор коллекций для Postman, созданные для учебных целей

Создано для вебинара https://www.youtube.com/watch?v=q9Xoic_14M0

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

## Установка Postman коллекций
1. Открыть Postman
2. Ctrl+O
3. В появившемся окне выбрать файл или папку
