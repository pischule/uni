NOT_SENT = 0
SENT = 1
CHECKED = 2


class Task:
    def __init__(self, grade=0, state=0):
        self.grade = grade
        self.state = state

    def __repr__(self):
        return f'Task(grade={self.grade!r}, state={self.state!r})'


class Student:
    def __init__(self, name, tasks, sum_grade, final_grade):
        self.name = name
        self.tasks = tasks
        self.sum_grade = sum_grade
        self.final_grade = final_grade

    def tasks_not_sent(self):
        return sum(1 for i in self.tasks if i.state == NOT_SENT)

    def tasks_sent(self):
        return sum(1 for i in self.tasks if i.state == SENT)

    def tasks_checked(self):
        return sum(1 for i in self.tasks if i.state == CHECKED)

    def tasks_total(self):
        return len(self.tasks)

    def __repr__(self):
        return f'Student(name={self.name!r}, tasks={self.tasks!r}, '\
            f'sum_grade={self.sum_grade!r}, final_grade={self.final_grade!r})'


if __name__ == '__main__':
    print(Task(10, True))
    print(Student('Ivan', [Task(0, 1), Task(10, 2)], 10, 10))
