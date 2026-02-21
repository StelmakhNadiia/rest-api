# REST API Library Project

## Лабораторна робота №1: Принципи REST API.Модель зрілості API RMM (Richardson Maturity Model).


### Опис
Реалізовано базове API для управління бібліотекою (сутність `Book`).



### ### Структура API (RMM Level 2)
- `GET /books` — Отримання списку книг - 200 OK
- `POST /books` — Додавання нової книги - 201 Created
- `PUT /books/<id>` — Оновлення даних книги - 200 OK
- `DELETE /books/<id>` — Видалення книги - 200 OK


### Запуск
1. Встановити залежності: `pip install flask`
2. Запустити сервер: `python app.py`