import asyncio
from vacancies_parser import fetch_vacancies
from candidates_parser import fetch_candidates
from db import create_database, save_vacancies, save_candidates


async def main():
    create_database()
    query = "Аналитик"
    pages_to_parse = 2

    print("Парсинг вакансий...")
    vacancies = await fetch_vacancies(query, pages_to_parse)
    print('Сохранение вакансий в базу данных...')
    save_vacancies(vacancies)

    for idx, vacancy in enumerate(vacancies, 1):
        print(f"Вакансия {idx}:")
        print(f"Название: {vacancy['title']}")
        print(f"Компания: {vacancy['company']}")
        print(f"Город: {vacancy['city']}")
        print(f"Опыт: {vacancy['experience']}")
        print(f"Зарплата: {vacancy['salary']}")
        print(f"Ссылка: {vacancy['link']}\n")

    print("Парсинг соискателей...")
    candidates = await fetch_candidates(query, pages_to_parse)
    print('Сохранение соискателей в базу данных...')
    save_candidates(candidates)

    for idx, candidate in enumerate(candidates, 1):
        print(f"Соискатель {idx}:")
        print(f"Название резюме: {candidate['title']}")
        print(f"Опыт: {candidate['experience']}")
        print(f"Зарплата: {candidate['salary']}")
        print(f"Ссылка: {candidate['link']}\n")


if __name__ == "__main__":
    asyncio.run(main())
