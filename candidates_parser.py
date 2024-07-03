
import aiohttp
from bs4 import BeautifulSoup
from vacancies_parser import to_number
import math
def convert_experience_to_float(experience_str):
    parts = experience_str.split()
    years = int(parts[0]) if parts[0].isdigit() else 0
    months = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
    total_months = years * 12 + months
    return math.ceil(total_months / 12)
async def fetch_candidates(query, pages=1):
    base_url = "https://hh.ru"
    search_url = f"{base_url}/search/resume?&logic=normal&pos=full_text&exp_period=all_time&exp_company_size=any&filter_exp_period=all_time&area=113&relocation=living_or_relocation&age_from=&age_to=&gender=unknown&salary_from=&salary_to=&currency_code=RUR&order_by=relevance&search_period=0&items_on_page=50&hhtmFrom=resume_search_form"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    candidates = []

    async with aiohttp.ClientSession() as session:
        for page in range(pages):
            params = {
                "text": query,
                "page": page
            }

            async with session.get(search_url, headers=headers, params=params) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'lxml')

                resume_blocks = soup.find_all('div', class_='wrapper--eiknuhp1KcZ2hosUJO7g')

                for resume in resume_blocks:
                    title_tag = resume.find('a', class_='bloko-link')
                    title = title_tag.text.strip()
                    link = 'https://hh.ru' + title_tag['href'] if title_tag and 'href' in title_tag.attrs else "Ссылка не указана"

                    experience_tag = resume.find('div', class_='content--uYCSpLiTsRfIZJe2wiYy')
                    experience_text = experience_tag.text.strip() if experience_tag else "Опыт не указан"
                    experience = convert_experience_to_float(experience_text)

                    salary_tag = resume.find('div', class_='bloko-text bloko-text_strong')
                    salary = salary_tag.text.strip() if salary_tag else "0"
                    salary = to_number(salary)
                    age_tag = resume.find(attrs={"data-qa":'resume-serp__resume-age'})
                    age_text = age_tag.text.strip() if age_tag else "0"
                    age = int(age_text.split()[0])

                    candidates.append({
                        "title": title,
                        "experience": experience,
                        "salary": salary,
                        'age': age,
                        "link": link
                    })
    return candidates
