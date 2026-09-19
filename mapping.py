class Student:
    def __init__(self, name):
        self.name = name

class Course:
    def __init__(self, name):
        self.name = name
        self.students = []

    def add_student(self, student):
     self.students.append(student)