# Library_Manager_PurePython

# Python Library Manager

Это консольное приложение для управления библиотекой книг, написанное на чистом Python без использования сторонних библиотек. Программа позволяет добавлять, удалять, искать книги, отображать их список, а также изменять статус книг.

## Описание

Программа позволяет управлять библиотекой книг в текстовом формате. Каждая книга имеет уникальный идентификатор, название, автора, год издания и статус. Статус книги может быть "в наличии" или "выдана". Все данные о книгах хранятся в текстовом файле.

### Возможности:

- **Добавление книги** — позволяет добавить книгу в библиотеку, указав её название, автора и год издания.
- **Удаление книги** — позволяет удалить книгу из библиотеки по её уникальному идентификатору.
- **Поиск книги** — позволяет искать книги по названию, автору или году издания.
- **Отображение всех книг** — отображает список всех книг в библиотеке.
- **Изменение статуса книги** — позволяет изменить статус книги на "в наличии" или "выдана".

## Особенности

- **Без сторонних библиотек** — все функции реализованы с использованием стандартных средств Python.
- **Проверка года издания** — программа проверяет, что год издания книги находится в диапазоне от 868 до 2024 года.
- **Обработка ошибок** — при попытке добавить, удалить или изменить книгу выводятся информативные сообщения.

## Структура проекта

- `library_manager.py` — главный файл приложения с реализацией всех функций.
- `library.txt` — файл, где хранятся данные о книгах.
При первом запуске library_manager.py и добавлении в нем книг он автоматически создаст файл library.txt

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/your-username/PythonLibraryManager.git

2. Перейдите в каталог проекта:

cd PythonLibraryManager


3. Запустите приложение:

python library_manager.py



Пример использования

После запуска программы вам будет предложено выбрать действие из следующих опций:

1. Добавить книгу


2. Удалить книгу


3. Поиск книги


4. Показать все книги


5. Изменить статус книги


6. Выйти



При добавлении книги вам будет предложено ввести название, автора и год издания. Если год издания не входит в допустимый диапазон, программа сообщит об ошибке. Вы сможете изменять статус книги и искать книги по различным параметрам.

Лицензия

Этот проект лицензируется под MIT License — подробности см. в файле LICENSE.

---

Спасибо за использование Python Library Manager! 🎉

Этот README содержит основные инструкции для пользователей, описание функционала приложения, структуру проекта и пример установки. Вы можете адаптировать его под свои нужды, например, добавив конкретные данные для лицензии или ссылку на свой репозиторий.

