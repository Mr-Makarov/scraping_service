import requests
import codecs
from bs4 import BeautifulSoup as BS

headers = {"user-agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
           "Accept": "*/*"}


def work_on_hh(url, city=None, language=None):
    jobs = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find_all('div', class_='serp-item')
            if main_div:
                for div in main_div:
                    title = div.find('h3', class_="bloko-header-section-3")
                    href = title.a['href']
                    content = div.find('div', {'class': "g-user-content"} )
                    company = div.find('a', class_="bloko-link bloko-link_kind-tertiary")

                    jobs.append({'title': title.text,
                                 'url': href,
                                 'description': content.text,
                                 'company': company.text,
                                 'city_id': city, 'language_id': language}
                                )
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


if __name__ == '__main__':
    url = "https://hh.ru/search/vacancy?text=Python&from=suggest_post&area=1"
    jobs, errors = work_on_hh(url)
    h = codecs.open('work.text', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()