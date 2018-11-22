from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Author(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    birthdate = models.DateField()
    city = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.firstname + ' ' + self.lastname + ' born ' + self.birthdate.strftime('%Y-%m-%d') + ' ' + self.city if self.city is not None else ''


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author)
    in_stock = models.BooleanField(default=True)
    numpages = models.IntegerField(default=0, validators=[MinValueValidator(50), MaxValueValidator(1000)])

    def __str__(self):
        return self.title + ' by ' + self.author.firstname + ' ' + self.author.lastname + ' ' + str(self.numpages) + ' pages'


class Student(User):
    PROVINCE_CHOICES = (
        ('AB', 'Alberta'),  # First value is stored in db, the second is descriptive
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    )
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Course(models.Model):
    course_no = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    textbook = models.ForeignKey(Book)
    students = models.ManyToManyField(Student, blank=True)

    def print_detail(self):
        out = 'Course title: ' + self.title
        out += ', course number: ' + str(self.course_no)
        out += ', textbook: ' + self.textbook.title
        return out

    def __str__(self):
        # return str(self.course_no) + ' ' + self.title + ' uses ' + self.textbook.title
        return 'Course title: ' + self.title + ', course number: ' + str(self.course_no) + ', textbook: ' + self.textbook.title


class Topic(models.Model):
    subject = models.CharField(max_length=100, unique=True)
    intro_course = models.BooleanField(default=True)
    NO_PREFERENCE = 0
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3
    TIME_CHOICES = (
        (0, 'No preference'),
        (1, 'Morning'),
        (2, 'Afternoon'),
        (3, 'Evening')
    )
    time = models.IntegerField(default=0, choices=TIME_CHOICES)
    num_responses = models.IntegerField(default=0)
    avg_age = models.IntegerField(default=20)

    def __str__(self):
        return self.subject

