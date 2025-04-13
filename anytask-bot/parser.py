from student import Student, Task
from scraper import AnytaskScraper
from constants import *


class StudentParser:

    def parseObject(self, students_object):
        students = []
        for s in students_object:
            tasks = [Task(float(t['grade']), t['state']) for t in s['tasks']]
            students.append(
                Student(s['name'], tasks, float(s['sumGrade']), s['finalGrade']))
        return students


if __name__ == '__main__':
    sp = StudentParser()
    ac = AnytaskScraper(ANYTASK_LOGIN, ANYTASK_PASSWORD)
    studObj = ac.get_object()
    print(sp.parseObject(studObj))
    pass
