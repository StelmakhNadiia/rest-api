# Library REST API (FastAPI) — Лабораторна робота №1

## Архітектура проєкту

### app/models/ — структури даних та сховище в пам'яті (List[Dict]).
### app/schemas/ — Pydantic-схеми для валідації запитів та відповідей.
### app/repository/ — шар доступу до даних (CRUD операції).
### app/services/ — бізнес-логіка (фільтрація за автором/статусом, сортування за назвою/роком).
### app/api/ — маршрутизація та обробка HTTP-запитів.


### ### Запуск проєкту
# Активація середовища
venv\Scripts\activate

# Встановлення залежностей
pip install -r requirements.txt

# Запуск сервера
uvicorn main:app --reload



### Тестування. Запуск автоматизованих юніт-тестів:
#### python -m pytest tests/test_books.py
