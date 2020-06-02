from scraper import AnytaskScraper
from parser import StudentParser
from decorators import cache
from constants import (ANYTASK_LOGIN, ANYTASK_PASSWORD)


class AnytaskClient():
    def __init__(self, login, password):
        self.login = login
        self.password = password

    @cache()
    def get_students(self):
        asc = AnytaskScraper(self.login, self.password)
        sp = StudentParser()
        return sp.parseObject(asc.get_object())

    def final_grade_report(self):
        students = self.get_students()
        lines = ['*Итоговая оценка:*', '`']
        for s in students:
            lines.append(f'{s.name:<25} {s.final_grade}')
        lines.append('`')
        return '\n'.join(lines)

    def sum_grade_report(self):
        lines = ['*Суммарный балл:*', '`']
        students = self.get_students()
        for s in students:
            lines.append(f'{s.name:<25} {s.sum_grade}')
        lines.append('`')
        return '\n'.join(lines)

    def done_report(self):
        students = self.get_students()
        lines = ['*Выполнение заданий:*', '`']
        for s in students:
            tmpstr = f'{s.tasks_sent() + s.tasks_checked()}/{s.tasks_total()}'
            lines.append(f'{s.name:<25} {tmpstr}')
        lines.append('`')
        return '\n'.join(lines)

    def group_stats(self):
        students = self.get_students()
        not_sent, sent, checked = 0, 0, 0
        for s in students:
            not_sent += s.tasks_not_sent()
            sent += s.tasks_sent()
            checked += s.tasks_checked()
        return sent, not_sent, checked



if __name__ == "__main__":
    ac = AnytaskClient(ANYTASK_LOGIN, ANYTASK_PASSWORD)
    print(ac.group_stats())
    print(ac.done_report())
    print(ac.sum_grade_report())
    print(ac.final_grade_report())
