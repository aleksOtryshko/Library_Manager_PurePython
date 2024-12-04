class Book:
    """Класс, представляющий книгу."""
    
    def __init__(self, book_id, title, author, year, status):
        self.book_id = book_id
        self.title = self._sanitize_input(title)
        self.author = self._sanitize_input(author)
        self.year = year
        self.status = status

    @staticmethod
    def _sanitize_input(input_string):
        """Удаляет спецсимволы и проверяет пустой ввод."""
        input_string = input_string.strip()
        allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,!?-"
        sanitized = ''.join(char for char in input_string if char in allowed_chars)
        if not sanitized:
            raise ValueError("Пустые значения и спец символы вводить нельзя.")
        return sanitized

    @staticmethod
    def validate_year(year):
        """Проверяет корректность года издания."""
        if not (868 <= year <= 2024):
            if year < 868:
                raise ValueError("Этого не может быть, так как первая книга напечатана в 868 году.")
            else:
                raise ValueError("Машина времени пока на ремонте, вы не могли достать книгу из будущего.")

    def to_text(self):
        """Преобразует книгу в строку для записи в файл."""
        return f"{self.book_id}|{self.title}|{self.author}|{self.year}|{self.status}"

    @staticmethod
    def from_text(text):
        """Создает объект книги из строки."""
        parts = text.strip().split("|")
        if len(parts) != 5:
            raise ValueError("Неверный формат данных в файле.")
        return Book(int(parts[0]), parts[1], parts[2], int(parts[3]), parts[4])


class Library:
    """Класс, управляющий библиотекой."""
    
    def __init__(self, storage_file):
        self.storage_file = storage_file
        self.books = self._load_books()

    def _load_books(self):
        """Загружает книги из файла."""
        try:
            with open(self.storage_file, "r") as file:
                return [Book.from_text(line) for line in file if line.strip()]
        except FileNotFoundError:
            return []

    def _save_books(self):
        """Сохраняет книги в файл."""
        with open(self.storage_file, "w") as file:
            for book in self.books:
                file.write(book.to_text() + "\n")

    def add_book(self, title, author, year):
        """Добавляет новую книгу."""
        try:
            Book.validate_year(year)
            book_id = len(self.books) + 1
            new_book = Book(book_id, title, author, year, "в наличии")
            self.books.append(new_book)
            self._save_books()
            print("Книга успешно добавлена.")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def remove_book(self, book_id):
        """Удаляет книгу по ID."""
        book = self._find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self._save_books()
            print("Книга успешно удалена.")
        else:
            print("Ошибка: Книга с таким ID не найдена.")

    def _find_book_by_id(self, book_id):
        """Находит книгу по ID."""
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def search_books(self, query):
        """Ищет книги по названию или автору."""
        results = [book for book in self.books if query.lower() in book.title.lower() or query.lower() in book.author.lower()]
        self._display_books(results)

    def display_books(self):
        """Выводит все книги."""
        if not self.books:
            print("Библиотека пуста.")
        else:
            self._display_books(self.books)

    def _display_books(self, books):
        """Выводит список книг."""
        for book in books:
            print(f"ID: {book.book_id} | Название: {book.title} | Автор: {book.author} | Год: {book.year} | Статус: {book.status}")

    def change_status(self, book_id, status):
        """Изменяет статус книги."""
        if status not in ["в наличии", "выдана"]:
            print("Ошибка: Некорректный статус.")
            return
        book = self._find_book_by_id(book_id)
        if book:
            book.status = status
            self._save_books()
            print("Статус книги успешно изменен.")
        else:
            print("Ошибка: Книга с таким ID не найдена.")


class LibraryApp:
    """Приложение для управления библиотекой."""
    
    def __init__(self, library):
        self.library = library

    def run(self):
        """Запуск приложения."""
        while True:
            self._display_menu()
            try:
                choice = input("Выберите действие: ").strip()
                if not choice:
                    raise ValueError("Ввод не может быть пустым.")
                match choice:
                    case "1":
                        title = input("Введите название книги: ").strip()
                        author = input("Введите автора книги: ").strip()
                        year = int(input("Введите год издания книги: ").strip())
                        self.library.add_book(title, author, year)
                    case "2":
                        book_id = int(input("Введите ID книги для удаления: ").strip())
                        self.library.remove_book(book_id)
                    case "3":
                        query = input("Введите поисковый запрос: ").strip()
                        self.library.search_books(query)
                    case "4":
                        self.library.display_books()
                    case "5":
                        book_id = int(input("Введите ID книги для изменения статуса: ").strip())
                        print("Выберите статус:")
                        print("1. в наличии")
                        print("2. выдана")
                        status_choice = input("Введите номер статуса: ").strip()
                        status = "в наличии" if status_choice == "1" else "выдана" if status_choice == "2" else None
                        if status:
                            self.library.change_status(book_id, status)
                        else:
                            print("Ошибка: Некорректный выбор статуса.")
                    case "6":
                        print("Выход.")
                        break
                    case _:
                        print("Ошибка: Некорректный выбор действия.")
            except ValueError as e:
                print(f"Ошибка: {e}")

    def _display_menu(self):
        """Выводит меню."""
        if not self.library.books:
            print("\nМеню:")
            print("1. Добавить книгу")
            print("6. Выход")
        else:
            print("\nМеню:")
            print("1. Добавить книгу")
            print("2. Удалить книгу")
            print("3. Найти книгу")
            print("4. Отобразить книги")
            print("5. Изменить статус книги")
            print("6. Выход")


# Запуск приложения
if __name__ == "__main__":
    library = Library("library.txt")
    app = LibraryApp(library)
    app.run()
