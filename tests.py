import unittest
import os
from library_manager import Book, Library

class TestBook(unittest.TestCase):

    def test_sanitize_input_valid(self):
        self.assertEqual(Book._sanitize_input("Test Book!"), "Test Book!")
        self.assertEqual(Book._sanitize_input("Book@123"), "Book123")
        self.assertEqual(Book._sanitize_input("   Clean Input!  "), "Clean Input!")

    def test_sanitize_input_invalid(self):
        with self.assertRaises(ValueError):
            Book._sanitize_input("@@@@")
        with self.assertRaises(ValueError):
            Book._sanitize_input("   ")

    def test_validate_year_valid(self):
        Book.validate_year(2000)  # Should pass without exception
        Book.validate_year(868)

    def test_validate_year_invalid(self):
        with self.assertRaises(ValueError):
            Book.validate_year(867)
        with self.assertRaises(ValueError):
            Book.validate_year(2025)

    def test_to_text(self):
        book = Book(1, "Test Book", "Author", 2000, "в наличии")
        self.assertEqual(book.to_text(), "1|Test Book|Author|2000|в наличии")

    def test_from_text_valid(self):
        text = "1|Test Book|Author|2000|в наличии"
        book = Book.from_text(text)
        self.assertEqual(book.book_id, 1)
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.author, "Author")
        self.assertEqual(book.year, 2000)
        self.assertEqual(book.status, "в наличии")

    def test_from_text_invalid(self):
        with self.assertRaises(ValueError):
            Book.from_text("Invalid|Data")


class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_library.txt"
        self.library = Library(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_book(self):
        self.library.add_book("Test Book", "Author", 2000)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Test Book")

    def test_remove_book(self):
        self.library.add_book("Test Book", "Author", 2000)
        book_id = self.library.books[0].book_id
        self.library.remove_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_search_books(self):
        self.library.add_book("Test Book", "Author", 2000)
        self.library.add_book("Another Book", "Another Author", 2010)
        results = self.library.search_books("Test")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Test Book")

    def test_change_status(self):
        self.library.add_book("Test Book", "Author", 2000)
        book_id = self.library.books[0].book_id
        self.library.change_status(book_id, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

    def test_load_and_save_books(self):
        self.library.add_book("Test Book", "Author", 2000)
        self.library._save_books()
        new_library = Library(self.test_file)
        self.assertEqual(len(new_library.books), 1)
        self.assertEqual(new_library.books[0].title, "Test Book")


if __name__ == "__main__":
    unittest.main()
