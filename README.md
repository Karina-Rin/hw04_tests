# hw04_tests

[![CI](https://github.com/yandex-praktikum/hw04_tests/actions/workflows/python-app.yml/badge.svg?branch=master)](https://github.com/yandex-praktikum/hw04_tests/actions/workflows/python-app.yml)

## Описание
Покрытие тестами проекта Yatube:
- Тестирование Models: «Unittest в Django: тестирование моделей»
- Тестирование URLs: «Unittest в Django: тестирование URLs»
- Проверка namespase: name и шаблонов: «Unittest в Django: тестирование Views»
- Тестирование контекста: «Unittest в Django: тестирование views»
- Дополнительная проверка при создании поста: «Unittest в Django: тестирование Views»
- Тестирование Forms: «Unittest в Django: тестирование Forms»

### Работа с репозиторим
1. Клонируем репозиторий на локальный компьютер:
```
git clone https://github.com/Karina-Rin/hw04_tests.git
```
2. Переносим в него всю папку `/yatube` из предыдущего репозитория.
3. Переходим в терминале в папку с проектом:
```
cd hw04_tests/
```
4. Развёртываем виртуальное окружение (работаем в VSCode):
* для Mac или Linux:
  ```
  $ python3 -m venv venv
  ```
* для Windows:
  ```
  $ python -m venv venv
  ```
5. Запускаем виртуальное окружение:
* для Mac или Linux:
  ```
  $ source venv/bin/activate
  ```
  
* для Windows:
  ```
  $ source venv/Scripts/activate
  ```
6. Устанавливаем зависимости из файла requirements.txt:
```
$ pip install -r requirements.txt
```
7. Запускаем тесты:
```
$ pytest
```

### Технологии:
* Python 3.7.1
* Pytest 6.2.5
* Flake8 4.0.1
* Django 2.2.8
* Django-debug-toolbar 2.2
