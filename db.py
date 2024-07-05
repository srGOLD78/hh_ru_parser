import sqlite3
import re


def create_database():
    with sqlite3.connect('my_database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
        DROP TABLE IF EXISTS vacancies;
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vacancies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255),
        company VARCHAR(255),
        salary VARCHAR(255),
        city VARCHAR(255),
        experience VARCHAR(255),
        link TEXT
        )
        ''')
        cursor.execute('''
        DROP TABLE IF EXISTS candidates;
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255),
        experience VARCHAR(255),
        salary VARCHAR(255),
        age INTEGER,
        link TEXT
        )
        ''')
        connection.commit()


def save_vacancies(vacancies):
    with sqlite3.connect('my_database.db') as connection:
        try:
            cursor = connection.cursor()
            for vacancy in vacancies:
                title = str(vacancy['title'])
                company = str(vacancy['company'])
                salary = str(vacancy['salary'])
                city = str(vacancy['city'])
                experience = str(vacancy['experience'])
                link = str(vacancy['link'])

                cursor.execute(
                    '''INSERT INTO vacancies (title, company, salary, city, experience, link) VALUES (?, ?, ?, ?, ?, ?)''',
                    (title, company, salary, city, experience, link)
                )
            connection.commit()
            print("Данные о вакансиях успешно сохранены в базу данных")
        except sqlite3.Error as e:
            print(f"Ошибка при сохранении вакансий: {e}")


def save_candidates(candidates):
    with sqlite3.connect('my_database.db') as connection:
        try:
            cursor = connection.cursor()
            for candidate in candidates:
                title = str(candidate['title'])
                experience = str(candidate['experience'])
                salary = str(candidate['salary'])
                age = int(candidate['age'])
                link = str(candidate['link'])

                cursor.execute(
                    '''INSERT INTO candidates (title, experience, salary, age, link) VALUES (?, ?, ?, ?, ?)''',
                    (title, experience, salary, age, link)
                )
            connection.commit()
            print("Данные о соискателях успешно сохранены в базу данных")
        except sqlite3.Error as e:
            print(f"Ошибка при сохранении соискателей: {e}")


def count_vacancies():
    with sqlite3.connect('my_database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM vacancies')
        count = cursor.fetchone()[0]
        return count


def count_candidates():
    with sqlite3.connect('my_database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM candidates')
        count = cursor.fetchone()[0]
        return count


def calculate_average_salary_vacancies():
    with sqlite3.connect('my_database.db') as connection:
        cursor = connection.cursor()
        query = "SELECT salary FROM vacancies WHERE salary IS NOT NULL"
        cursor.execute(query)
        salary_vacancies = cursor.fetchall()

        if not salary_vacancies:
            print("Нет доступных данных о зарплатах для расчета.")
            return None

        total_salary = 0
        count = 0

        for salary in salary_vacancies:
            salary_str = salary[0]
            if '-' in salary_str:
                min_salary, max_salary = salary_str.split('-')
                min_salary = min_salary.replace(',', '').strip()
                max_salary = max_salary.replace(',', '').strip()
                try:
                    avg_salary = (float(min_salary) + float(max_salary)) / 2
                except ValueError:
                    continue
            else:
                salary_val = salary_str.replace(',', '').strip()
                try:
                    avg_salary = float(salary_val)
                except ValueError:
                    continue

            total_salary += avg_salary
            count += 1

        if count == 0:
            print("Нет корректных данных для расчета средней зарплаты.")
            return None

        average_salary = total_salary / count
        return average_salary


def calculate_average_salary_candidates():
    with sqlite3.connect('my_database.db') as connection:
        cursor = connection.cursor()
        query = "SELECT salary FROM candidates WHERE salary IS NOT NULL"
        cursor.execute(query)
        salary_candidates = cursor.fetchall()

        if not salary_candidates:
            print("Нет доступных данных о зарплатах для расчета.")
            return None

        total_salary = 0
        count = 0

        for salary in salary_candidates:
            salary_str = salary[0].replace('\xa0', '')
            salary_val = re.sub(r'[^\d.]', '', salary_str)
            try:
                avg_salary = float(salary_val)
            except ValueError:
                continue

            total_salary += avg_salary
            count += 1

        if count == 0:
            print("Нет корректных данных для расчета средней зарплаты.")
            return None

        average_salary = total_salary / count
        return average_salary
        
def remove_duplicates_vacancies():
    with sqlite3.connect('my_database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            DELETE FROM vacancies
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM vacancies
                GROUP BY title, company
            )
        ''')
        connection.commit()
        print("Дубликаты удалены успешно")
def remove_duplicates_candidates():
    with sqlite3.connect('my_database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            DELETE FROM candidates
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM vacancies
                GROUP BY title, company
            )
        ''')
        connection.commit()
        print("Дубликаты удалены успешно")



def get_filtered_vacancies(filters):
    with sqlite3.connect('my_database.db') as connection:
        cursor = connection.cursor()

        query = 'SELECT * FROM vacancies WHERE 1=1'
        params = []

        if 'city' in filters:
            query += ' AND city = ?'
            params.append(filters['city'])

        if 'salary' in filters:
            salary_min, salary_max = filters['salary']
            query += ' AND CAST(REPLACE(REPLACE(salary, "от ", ""), " ", "") AS INTEGER) BETWEEN ? AND ?'
            params.extend([salary_min, salary_max])

        if 'experience' in filters:
            experience_min, experience_max = filters['experience']
            query += ' AND CAST(REPLACE(REPLACE(experience, "от ", ""), " ", "") AS INTEGER) BETWEEN ? AND ?'
            params.extend([experience_min, experience_max])

        cursor.execute(query, params)
        rows = cursor.fetchall()
        filtered_vacancies = []

        for row in rows:
            filtered_vacancies.append({
                'id': row[0],
                'title': row[1],
                'company': row[2],
                'salary': row[3],
                'city': row[4],
                'experience': row[5],
                'link': row[6]
            })

        return filtered_vacancies


def get_filtered_candidates(filters):
    with sqlite3.connect('my_database.db') as connection:
        cursor = connection.cursor()

        query = 'SELECT * FROM candidates WHERE 1=1'
        params = []

        if 'experience' in filters:
            experience_min, experience_max = filters['experience']
            query += ' AND CAST(REPLACE(REPLACE(experience, "от ", ""), " ", "") AS INTEGER) BETWEEN ? AND ?'
            params.extend([experience_min, experience_max])

        if 'salary' in filters:
            salary_min, salary_max = filters['salary']
            query += ' AND CAST(REPLACE(REPLACE(salary, "₽", ""), " ", "") AS INTEGER) BETWEEN ? AND ?'
            params.extend([salary_min, salary_max])

        if 'age' in filters:
            age_min, age_max = filters['age']
            query += ' AND age BETWEEN ? AND ?'
            params.extend([age_min, age_max])

        cursor.execute(query, params)
        rows = cursor.fetchall()
        filtered_candidates = []

        for row in rows:
            print(f"DEBUG: Found candidate with salary {row[3]}")
            filtered_candidates.append({
                'id': row[0],
                'title': row[1],
                'experience': row[2],
                'salary': row[3],
                'age': row[4],
                'link': row[5]
            })

        return filtered_candidates
