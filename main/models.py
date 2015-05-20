from django.db import models
from polymorphic import PolymorphicModel

# Doc: http://www.apidev.fr/blog/2012/01/12/heritage-de-modele-avec-django/

class User(PolymorphicModel):
    username = models.CharField(primary_key=True, max_length=255)
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)

    def __str__(self):
        return "{0} ({1} {2})".format(self.username, self.lastname, self.firstname)


class Admin(User):
    pass


class Teacher(User):
    groups = models.ManyToManyField('Group')

    def __str__(self):
        return "{0} ({1})".format(super(Teacher, self).__str__(), self.group)


class Student(User):
    group = models.ForeignKey('Group')

    def __str__(self):
        return "{0} ({1})".format(super(Student, self).__str__(), self.group)


class Group(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    exercises = models.ManyToManyField('Exercise')

    def __str__(self):
        return self.group_name


class Activity(models.Model):  # Une activit� est compos�e de plusieurs exercices
    name = models.CharField(primary_key=True, max_length=255)
    date = models.DateTimeField()
    multi_attempts = models.BooleanField()  # tentatives multiples ?
    interactive_correction = models.BooleanField()  # correction interactive ? utile en materelle

    teacher = models.ForeignKey('Teacher')

    def __str__(self):
        return self.name


class Exercise(models.Model):
    exercise_json = models.CharField(max_length=16384)#TODO
    activity = models.ForeignKey('Activity')


class CorrectionElement(models.Model):
    index = models.IntegerField()
    content = models.CharField(max_length=255)
    exercise = models.ForeignKey('Exercise')


class Reply(models.Model):
    date = models.DateTimeField()

    exercise = models.ForeignKey('Exercise')
    student = models.ForeignKey('Student')

    index = models.IntegerField()
    content = models.CharField(max_length=255)

    def __str__(self):
        return "{0} {1} ({2})".format(self.student, self.exercise, self.date)