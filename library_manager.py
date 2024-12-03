# Класс для представления книги
class Book:
    def __init__(self, book_id, title, author, year, status="в наличии"):
        self.book_id = book_id
        self.title = self._sanitize_input(title)
        self.author = self._sanitize_input(author)
        self.year = year
        self.status = status

    @staticmethod
    def _sanitize_input(value):
        """Удаляет потенциально вредоносный код из строки"""
        prohibited_chars = ['<', '>', '{', '}', ';', '"', "'"]
        for char in prohibited_chars:
            value = value.replace(char, "")
        return value.strip()

    def to_text(self):
        """Преобразует объект книги в строку для хранения в файле"""
        return f"{self.book_id},{self.title},{self.author},{self.year},{self.status}"

    @staticmethod
    def from_text(text):
    """Создает объект книги из строки"""
        try:
        # Разбиваем строку на части
            parts = text.strip().split(",")
        
        # Проверяем, что частей ровно 5
            if len(parts) != 5:
                raise ValueError("Некорректный формат строки. Ожидалось 5 частей, разделенных запятыми.")
        
        # Преобразуем и возвращаем объект книги
            return Book(int(parts[0]), parts[1], parts[2], int(parts[3]), parts[4])
         except ValueError as e:
             print(f"Ошибка: {e}")
             return None
         except IndexError:
             print("Ошибка: Некорректный формат строки. Проверьте входные данные.")
             return None
# Класс для управления библиотекой
class LibraryManager:
    def __init__(self, file_name):
        self.file_name = file_name
        self.books = self._load_books()

    def _load_books(self):
        """Загружает книги из файла"""
        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                return [Book.from_text(line) for line in file]
        except FileNotFoundError:
            return []

    def _save_books(self):
        """Сохраняет книги в файл"""
        with open(self.file_name, "w", encoding="utf-8") as file:
            for book in self.books:
                file.write(book.to_text() + "\n")

    def add_book(self, title, author, year):
        """Добавляет книгу в библиотеку"""
        if year < 868:
            raise ValueError("Этого не может быть, так как первая книга напечатана в 868 году.")
        elif year > 2024:
            raise ValueError("Машина времени пока на ремонте. Введите корректную дату.")
        
        book_id = self._generate_id()
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self._save_books()

    def delete_book(self, book_id):
        """Удаляет книгу из библиотеки"""
        book = self._find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self._save_books()
        else:
            raise ValueError(f"Книга с ID {book_id} не найдена.")

    def search_books(self, query):
        """Ищет книги по названию, автору или году"""
        query = Book._sanitize_input(query)
        results = [book for book in self.books if query.lower() in book.title.lower() or query.lower() in book.author.lower() or query == str(book.year)]
        return results

    def change_status(self, book_id, status):
        """Изменяет статус книги"""
        if status not in ["в наличии", "выдана"]:
            raise ValueError("Некорректный статус. Выберите из: 'в наличии' или 'выдана'.")
        book = self._find_book_by_id(book_id)
        if book:
            book.status = status
            self._save_books()
        else:
            raise ValueError(f"Книга с ID {book_id} не найдена.")

    def display_books(self):
        """Возвращает список всех книг"""
        return self.books

    def _generate_id(self):
        """Генерирует уникальный ID для новой книги"""
        return max([book.book_id for book in self.books], default=0) + 1

    def _find_book_by_id(self, book_id):
        """Ищет книгу по ID"""
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None


# Класс для взаимодействия с пользователем
class LibraryApp:
    def __init__(self, manager):
        self.manager = manager

    def run(self):
        """Главный цикл приложения"""
        while True:
            try:
                # Проверка на наличие книг в библиотеке
                if not self.manager.books:
                    print("\nМеню:")
                    print("1. Добавить книгу")
                    print("2. Выход")
                    action = input("Выберите действие: ")
                    if action == "1":
                        self._add_book()
                    elif action == "2":
                        print("До свидания!")
                        break
                    else:
                        print("Неверный выбор. Попробуйте снова.")
                else:
                    print("\nМеню:")
                    print("1. Добавить книгу")
                    print("2. Удалить книгу")
                    print("3. Найти книгу")
                    print("4. Показать все книги")
                    print("5. Изменить статус книги")
                    print("6. Выход")
                    action = input("Выберите действие: ")

                    if action == "1":
                        self._add_book()
                    elif action == "2":
                        self._delete_book()
                    elif action == "3":
                        self._search_books()
                    elif action == "4":
                        self._display_books()
                    elif action == "5":
                        self._change_status()
                    elif action == "6":
                        print("До свидания!")
                        break
                    else:
                        print("Неверный выбор. Попробуйте снова.")
            except Exception as e:
                print(f"Ошибка: {e}")

    def _add_book(self):
        """Добавляет книгу"""
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        try:
            year = int(input("Введите год издания книги: "))
            self.manager.add_book(title, author, year)
            print("Книга успешно добавлена!")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def _delete_book(self):
        """Удаляет книгу"""
        try:
            book_id = int(input("Введите ID книги для удаления: "))
            self.manager.delete_book(book_id)
            print("Книга успешно удалена!")
        except ValueError :
            print(f"Ошибка: Введите номер ID цифрами!")

    def _search_books(self):
        """Ищет книги"""
        query = input("Введите название, автора или год книги для поиска: ")
        results = self.manager.search_books(query)
        if results:
            print("Найденные книги:")
            for book in results:
                print(f"{book.book_id}: {book.title} ({book.author}, {book.year}) - {book.status}")
        else:
            print("Книги не найдены.")

    def _display_books(self):
        """Выводит список всех книг"""
        books = self.manager.display_books()
        print("Список всех книг:")
        for book in books:
            print(f"{book.book_id}: {book.title} ({book.author}, {book.year}) - {book.status}")

    def _change_status(self):
        """Изменяет статус книги"""
        try:
            book_id = int(input("Введите ID книги для изменения статуса: "))
            print("Выберите статус:")
            print("1. в наличии")
            print("2. выдана")
            status = input("Введите номер статуса: ")
            if status == "1":
                self.manager.change_status(book_id, "в наличии")
            elif status == "2":
                self.manager.change_status(book_id, "выдана")
            else:
                print("Некорректный выбор статуса.")
        except ValueError :
            print(f"Ошибка: Введите ID цифрами!")


# Запуск приложения
if __name__ == "__main__":
    manager = LibraryManager("library.txt")
    app = LibraryApp(manager)
    app.run()
