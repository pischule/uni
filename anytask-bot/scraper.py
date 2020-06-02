import requests
import json

from bs4 import BeautifulSoup

from constants import *

LOGIN_URL = 'https://anytask.org/accounts/login/'
TABLE_URL = 'https://anytask.org/course/667/gradebook/'


class AnytaskScraper:
    NOT_SENT = 0
    SENT = 1
    CHECKED = 2

    GREEN = '#65e31b'
    GREY = '#818a91'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_page_html(self):
        form_data = {'username': self.username,
                     'password': self.password, 'csrfmiddlewaretoken': ''}
        headers = {'Referer': LOGIN_URL}

        table_html = ''
        with requests.Session() as s:
            r = s.get(LOGIN_URL)

            soup = BeautifulSoup(r.text, 'html.parser')
            token = soup.find('input')['value']
            form_data['csrfmiddlewaretoken'] = token

            r = s.post(LOGIN_URL, data=form_data, headers=headers)
            r = s.get(TABLE_URL)

            table_html = r.content
        return table_html

    def get_json(self):
        stud_object = self.get_object()
        return json.dumps(stud_object)

    @staticmethod
    def _color_to_state(color):
        if color == AnytaskScraper.GREEN:
            return AnytaskScraper.CHECKED
        elif color == AnytaskScraper.GREY:
            return AnytaskScraper.NOT_SENT
        return AnytaskScraper.SENT

    def get_object(self):
        # for debug purposes
        # html = open('page.html').read()

        html = self.get_page_html()
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('tbody')
        studentsArr = []
        for row in table.find_all('tr'):
            cols = row.find_all('td')

            tasks = []
            for task in cols[2:-2]:
                color = task.span.get('style')[18:-1].lower()
                tasks.append({
                    'grade': task.text.strip(),
                    'state': AnytaskScraper._color_to_state(color)
                })

            studentObject = {
                'name': cols[1].text.strip(),
                'tasks': tasks,
                'sumGrade': cols[-2].text.strip(),
                'finalGrade': cols[-1].text.strip()
            }

            studentsArr.append(studentObject)
        return studentsArr


if __name__ == "__main__":
    ascr = AnytaskScraper(ANYTASK_LOGIN, ANYTASK_PASSWORD)
    print(ascr.get_json())
    pass
