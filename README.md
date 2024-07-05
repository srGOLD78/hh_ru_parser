# Проект: Бот-парсер текущих вакансий с использованием  BeautifulSoup

## Описание
Данный проект представляет собой бота, который парсит текущие вакансии с сайта, предоставляя пользователям актуальную информацию о вакансиях в интересующих их областях. Проект разработан с использованием Telegram bota для создания пользовательского интерфейса и BeautifulSoup для парсинга данных.

## Функциональные требования

1. **Парсинг вакансий**: 
   - Автоматический сбор данных о вакансиях с указанного сайта.
   - Парсинг данных таких, как название вакансии, компания, местоположение и другие важные характеристики.

2. **Обработка данных**: 
   - Фильтрация и структурирование собранных данных.
   - Сохранение данных в базу данных для дальнейшего анализа или использования(Саму базу данных можно посмотреть в SQLite Studio).

3. **Гибкость и расширяемость**:
   - Возможность легко изменить телеграм бота или добавлять новые поля для парсинга.
  
## Структура проекта
```plaintext
hh_ru_parser/
├── .venv/
├── bot.py
├── vacancies_parser.py
├── candidates_parser.py
├── db.py
├── my_database.db
├── requirments.txt
├── test.py
├── Dockerfile
└── docker-compose.yml
```

## Технологии

В проектах этого репозитория используются различные технологии, включая, но не ограничиваясь:

- Python
- Docker
- Telegram API

## Установка

Для быстрой установки вы можете использовать Docker Compose. Вот пошаговая инструкция:

1.  Установите [Docker Compose Desktop](https://www.docker.com/products/docker-desktop).
2.  В корневой папке проекта откройте командную строку (введите `cmd` в строке поиска вверху директории).
3.  Введите команду:
   ```sh
   git clone https://github.com/srGOLD78/hh_ru_parser.git
   ```
4.  Перейдите в директорию проекта:
   ```sh
   cd hh_ru_parser
   ```
5.  Установите зависимости, перечисленные в файле requirements.txt.
   ```sh
   pip install -r requirements.txt
   ```
6.  Введите команду:
   ```sh
   docker-compose up --build
   ```
Чтобы остановить контейнер нажмите ctrl + c
7. Сам бот по моем токену: https://t.me/Parserhh23Bot
Вы можете создать свой токен через BotFather и вставить в код место TOKEN:'ваш токен'
8.  Бот работает, напишите команду `/start`.

## Описание файлов
- `bot.py`: Основной код бота.
- `vacancies_parser.py`: Скрипт для парсинга вакансий.
- `candidates_parser.py`: Скрипт для парсинга соискателей.
- `db.py`: Основной файл для создания бд, в котором находятся: скрипт для подсчёта средних значений зарплат,скрипт для удаления дубликатов,скрипт для фильтрации вакансий и кандидатов в бд.
- `my_database.db`: Файл с базой данных
- `test.py`: Скрипт для проведения тестов функций.

    
     

     
