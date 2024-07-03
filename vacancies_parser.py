import aiohttp
from bs4 import BeautifulSoup


def to_number(s: str) -> str:
    s1 = ''
    for c in s:
        if c.isnumeric() or c == '–' or c == '-':
            s1 += c
    return s1

async def fetch_vacancies(query, filters=None, pages=1):
    base_url = "https://hh.ru"
    search_url = f"{base_url}/search/vacancy?L_save_area=true&text=&excluded_text=&area=113&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=50&hhtmFrom=vacancy_search_filter"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    vacancies = []

    async with aiohttp.ClientSession() as session:
        for page in range(pages):
            params = {
                "text": query,
                "page": page
            }

            async with session.get(search_url, headers=headers, params=params) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'lxml')

                job_blocks = soup.find_all('div', class_='vacancy-search-item__card')

                for job in job_blocks:
                    title_tag = job.find('a', class_='bloko-link')
                    title = title_tag.text.strip()
                    link = title_tag['href'] if title_tag and 'href' in title_tag.attrs else "Ссылка не указана"

                    company_tag = job.find('a', class_='bloko-link bloko-link_kind-secondary')
                    company = company_tag.text.strip() if company_tag else "Компания не указана"

                    salary_tag = job.find('span',
                                          class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh')
                    salary = salary_tag.text.strip() if salary_tag else "Зарплата не указана"
                    salary = to_number(salary)
                    experience_tag = job.find('span',
                                              class_='label--rWRLMsbliNlu_OMkM_D3 label_light-gray--naceJW1Byb6XTGCkZtUM')
                    experience = experience_tag.text.strip() if experience_tag else "Опыт не указан"
                    experience = to_number(experience)
                    city_tag = job.find(attrs={"data-qa": "vacancy-serp__vacancy-address_narrow"})
                    city = city_tag.text.strip() if city_tag else "Город не указан"

                    vacancies.append({
                        "title": title,
                        "company": company,
                        "salary": salary,
                        'experience': experience,
                        'city': city,
                        "link": link
                    })
    return vacancies
