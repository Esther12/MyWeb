from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from myapp.models import Author, Book, Course, Topic, Student
from .forms import TopicForm, InterestForm


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.first_name = username
        user.save()
        return render(request, 'myapp/index.html')
    else:
        return render(request, 'myapp/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required
def mycourses(request):
    print(request.user.id)
    res = {}
    user = Student.objects.filter(pk=request.user.id)
    if user.count() == 0:
        res = {'msg': 'You are not a student!'}
    else:
        courses = Course.objects.filter(students=user)
        res = {'courses': courses}

    return render(request, 'myapp/mycourses.html', res)


def index(request):
    courselist = Course.objects.all().order_by('title')[:10]
    return render(request, 'myapp/index.html', {'courselist': courselist})


def about(request):
    return render(request, 'myapp/about0.html')


def detail(request, course_no):
    course = get_object_or_404(Course, course_no=course_no)

    return render(request, 'myapp/detail0.html', {'course': course})


def topics(request):
    topiclist = Topic.objects.all()[:10]
    return render(request, 'myapp/topics.html', {'topiclist': topiclist})


def addtopic(request):
    topiclist = Topic.objects.all()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.num_responses = 1
            topic.save()
            return HttpResponseRedirect(reverse('myapp:topics'))
    else:
        form = TopicForm()
        return render(request, 'myapp/addtopic.html', {'form': form, 'topiclist': topiclist})


def topicdetail(request, topic_id):
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid() and form.cleaned_data['interested']:
            topic = get_object_or_404(Topic, id=topic_id)
            topic.avg_age = (topic.avg_age * topic.num_responses + form.cleaned_data['age']) / (topic.num_responses + 1)
            print(topic.avg_age)
            topic.num_responses = topic.num_responses + 1
            topic.save()
        return HttpResponseRedirect(reverse('myapp:topics'))
    else:
        topic = get_object_or_404(Topic, id=topic_id)
        form = InterestForm()
        return render(request, 'myapp/topicdetail.html', {'topic': topic, 'form': form})

