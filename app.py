from flask import Flask, jsonify, request

app = Flask(__name__)


books = {
    1: {
        "id": 1,
        "title": "Intermezzo",
        "description": "Психологічна новела про втому від суспільства",
        "author": "Михайло Коцюбинський",
        "year": 1908,
        "genre": "Новела",
        "pages": 20
    }
}


next_book_id = 2

@app.route('/')
def welcome():
    return "Ласкаво просимо до API бібліотеки!"

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(list(books.values())), 200

@app.route('/books', methods=['POST'])
def create_book():
    global next_book_id
    data = request.get_json()

    # Валідація: перевіряємо, чи передана назва книги 
    if not data or 'title' not in data:
        return jsonify({"error": "Назва книги (title) є обов'язковим полем"}), 400

    # Створюємо новий об'єкт книги
    new_book = {
        "id": next_book_id,
        "title": data.get('title'),
        "description": data.get('description', ''),
        "author": data.get('author', 'Невідомий автор'),
        "year": data.get('year'),
        "genre": data.get('genre', 'Інше'),
        "pages": data.get('pages', 0)
    }

    # Зберігаємо в нашу структуру даних
    books[next_book_id] = new_book
    next_book_id += 1

    # Повертаємо створений об'єкт та статус 201 Created
    return jsonify(new_book), 201


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    # Шукаємо книгу за ключем у нашому словнику
    book = books.get(book_id)
    
    if book:
        return jsonify(book), 200
    
    # Якщо ідентифікатор не знайдено, повертаємо 404 
    return jsonify({"error": "Книгу не знайдено"}), 404

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if book_id not in books:
        return jsonify({"error": "Книгу не знайдено"}), 404
    
    data = request.get_json()
    
    # Валідація: назва обов'язкова для повного оновлення (PUT)
    if not data or 'title' not in data:
        return jsonify({"error": "Поле 'title' обов'язкове для оновлення"}), 400

    # Оновлюємо всі поля  
    books[book_id].update({
        "title": data.get('title'),
        "description": data.get('description', books[book_id].get('description')),
        "author": data.get('author', books[book_id].get('author')),
        "year": data.get('year', books[book_id].get('year')),
        "genre": data.get('genre', books[book_id].get('genre')),
        "pages": data.get('pages', books[book_id].get('pages'))
    })
    
    return jsonify(books[book_id]), 200

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    if book_id in books:
        del books[book_id]
        return jsonify({"message": "Книгу успішно видалено"}), 200
    
    return jsonify({"error": "Книгу не знайдено"}), 404



if __name__ == '__main__':
    app.run(debug=True)