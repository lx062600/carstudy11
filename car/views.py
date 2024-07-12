from django.contrib.auth.forms import UserCreationForm
from django.core.cache import cache
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import random
from .models import Question, post, Comment
import json
from django.utils import timezone
from django.db.models import Q
import datetime
from .models import CustomUser


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = CustomUser.objects.filter(username=username).first()

        if user is not None:
            if user.password == password:
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                return redirect('car:index')
            else:
                return render(request, 'login.html', {'error': '密码不正确'})
        else:
            new_user = CustomUser(username=username, password=password)
            new_user.save()
            request.session['user_id'] = new_user.id
            request.session['username'] = new_user.username
            return redirect('car:index')

    return render(request, 'login.html')


def index(request):
    username = request.CustomUser.username if request.user.is_authenticated else None
    context = {
        'username': username,
    }
    return render(request, 'index.html', context)

def keyi(request):
    return render(request, 'ke1.html')

def keer(request):
    return render(request, 'ke2.html')

def kesan(request):
    return render(request, 'ke3.html')
def kesi(request):
    return render(request, 'ke4.html')

def sequential_view(request):
    return redirect('car:show_question',question_id=1)

def show_question(request, question_id):

   current_question = get_object_or_404(Question, pk=question_id)

   titles = json.loads(current_question.title)
   descriptions = json.loads(current_question.descarray)
   answer = current_question.answer
   if len(titles) != len(descriptions):
       raise ValueError("Title and descarray lengths do not match")

   paired_options = dict(zip(titles, descriptions))

   try:
       previous_question = Question.objects.filter(Q(pk__lt=question_id)).order_by('-pk').first()
   except Question.DoesNotExist:
       previous_question = None

   try:
       next_question = Question.objects.filter(Q(pk__gt=question_id)).order_by('pk').first()
   except Question.DoesNotExist:
       next_question = None

   context = {
       'question': current_question,
       'paired_options': paired_options,
       'previous_question': previous_question,
       'next_question': next_question,
       'answer':answer,
   }
   return render(request, 'sequential.html', context)


def submit_answer(request, question_id):
    if request.method == 'POST':
        current_question = get_object_or_404(Question, pk=question_id)
        user_answer = request.POST.get('answer')
        correct_answer = current_question.answer

        is_correct = user_answer == correct_answer

        skill_explain = current_question.skillexplain
        answer_text = current_question.answer

        next_question_id = current_question.pk + 1
        next_question = get_object_or_404(Question, pk=next_question_id) if Question.objects.filter(
            pk=next_question_id).exists() else None
        next_url = next_question.get_absolute_url() if next_question else reverse('some_default_view')

        return JsonResponse({
            'is_correct': is_correct,
            'skill_explain': skill_explain,
            'answer': answer_text,
            'next_url': next_url,
        })
    else:
        return HttpResponseRedirect(reverse('car:show_question', args=(question_id,)))


def show_chapter(request, chapter_id):
    return render(request, 'chapter.html')


def random_question(request):
    last_question_id = request.session.get('last_question_id', None)

    questions = Question.objects.all()
    if questions.exists():
        if last_question_id:
            try:
                last_question = questions.get(id=last_question_id)
                questions = questions.exclude(id=last_question_id)
            except Question.DoesNotExist:
                pass
        random_question = random.choice(questions)
        request.session['last_question_id'] = random_question.id
    
        titles = json.loads(random_question.title)
        desc = json.loads(random_question.descarray)
        answer = random_question.answer
        if len(titles) != len(desc):
            raise ValueError("Title and descarray lengths do not match")

        options = dict(zip(titles, desc))

        # 构造上下文
        context = {
            'question_id': random_question.id,
            'question_title': random_question.title,
            'options': options,
            'correct_answer': answer,
            'question_question':random_question.question,
            'question_url':random_question.url,
            'skill_explain':random_question.skillexplain,
        }

        # 渲染模板
        return render(request, 'random.html', context)

def get_question_context(question):
    # 解析title和descarray字段以获取选项和描述的对应关系
    titles = json.loads(question.title)
    desc = json.loads(question.descarray)
    if len(titles) != len(desc):
        raise ValueError("Title and descarray lengths do not match")

    options = dict(zip(titles, desc))

    # 构造上下文
    context = {
        'question_id': question.id,
        'question_title': question.title,  # 假设title字段存储的是选项标题的JSON字符串
        'options': options,
        'correct_answer': question.answer,  # 假设answer字段存储正确答案
        'question_question': question.question,  # 假设question字段存储问题文本
        'question_url': random_question.url,
        'skill_explain': random_question.skillexplain,
    }
    return context

def previous_question(request):
    last_question_id = request.session.get('last_question_id', None)
    if not last_question_id:
        return HttpResponseRedirect(reverse('car:random_question'))

    questions = Question.objects.all()
    if questions.exists():
        try:
            previous_question = questions.get(id=last_question_id)
        except Question.DoesNotExist:
            return HttpResponseRedirect(reverse('car:random_question'))
        previous_question_ids = list(questions.values_list('id', flat=True))
        index = previous_question_ids.index(last_question_id)
        if index == 0:
            next_question_id = previous_question_ids[-1]
        else:
            next_question_id = previous_question_ids[index - 1]

        request.session['last_question_id'] = next_question_id

        return random_question(request)

    return HttpResponseRedirect(reverse('car:random_question'))

def next_question(request):
    current_question_id = request.session.get('current_question_id')
    if not current_question_id:
        return redirect(reverse('car:random_question'))

    questions = Question.objects.exclude(id=current_question_id)
    if questions.exists():
        next_question = random.choice(questions)

        request.session['current_question_id'] = next_question.id

        context = get_question_context(next_question)
        return render(request, 'random.html', context)

    else:
        # 如果没有更多问题，可以重定向回随机问题页面或者显示一个消息
        return redirect(reverse('car:random_question'))


def start_exam(request):
    exam_questions = cache.get('exam_questions')
    sorted_questions = []

    if exam_questions is None:
        # 缓存中没有考试题目，从数据库中获取所有题目
        all_questions = Question.objects.all()
        exam_questions = random.sample(list(all_questions), 100)
        for i, question in enumerate(exam_questions,start=1):
            setattr(question, 'le', i)

        sorted_questions = sorted(exam_questions, key=lambda x: x.le)
        cache.set('exam_questions', sorted_questions,3600) #缓存1小时
    else:
        sorted_questions = exam_questions

    current_le = int(request.GET.get('le', 1))
    current_question = next((q for q in sorted_questions if q.le == current_le), None)
    if current_question is None:
        return HttpResponseBadRequest("Invalid question number")

    next_le = current_le + 1 if current_le < len(sorted_questions) else 1
    prev_le = current_le - 1 if current_le > 1 else len(sorted_questions)

    try:
        titles = json.loads(current_question.title)
        desc = json.loads(current_question.descarray)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON in question data")

    if len(titles) != len(desc):
        return HttpResponseBadRequest("Title and descarray lengths do not match")

    options = dict(zip(titles, desc))

    question_numbers = [[(i * 10) + j + 1 for j in range(10)] for i in range(10)]
    next_questions_url = reverse('car:next_questions')

    request.session['current_le'] = current_le

    context = {
        'question': current_question,
        'question_answer':current_question.answer,
        'options': options,
        'current_le': current_le,
        'total_questions': len(sorted_questions),
        'next_le': next_le,
        'prev_le': prev_le,
        'question_numbers': question_numbers,
        'next_questions_url': next_questions_url,
        'question_url': current_question.url,
        'skill_explain': current_question.skillexplain,
    }

    return render(request, 'exam.html', context)


def next_questions(request):
    current_le = request.session.get('current_le')
    exam_questions = cache.get('exam_questions')
    if exam_questions is None:
        return HttpResponseBadRequest("No questions available in cache.")

    sorted_questions = sorted(exam_questions, key=lambda x: x.le)
    next_le = current_le + 1 if current_le < len(sorted_questions) else 1
    next_url = reverse('car:exam_questions') + '?le=' + str(next_le)
    return redirect(reverse('car:'))


def previous_questions(request):
    current_le = request.session.get('current_le')
    exam_questions = cache.get('exam_questions')
    if exam_questions is None:
        return HttpResponseBadRequest("No questions available in cache.")

    sorted_questions = sorted(exam_questions, key=lambda x: x.le)
    prev_le = current_le - 1 if current_le > 1 else len(sorted_questions)
    return HttpResponseRedirect(f'?le={prev_le}')


def pk(request):
    pk_questions = cache.get('pk_questions')
    sorted_questions = []

    if pk_questions is None:
        # 缓存中没有考试题目，从数据库中获取所有题目
        all_questions = Question.objects.all()
        pk_questions = random.sample(list(all_questions), 10)
        for i, question in enumerate(pk_questions, start=1):
            setattr(question, 'le', i)

        sorted_questions = sorted(pk_questions, key=lambda x: x.le)
        cache.set('exam_questions', sorted_questions, 360)  # 缓存1小时
    else:
        sorted_questions = pk_questions

    current_le = int(request.GET.get('le', 1))
    current_question = next((q for q in sorted_questions if q.le == current_le), None)
    if current_question is None:
        return HttpResponseBadRequest("Invalid question number")

    next_le = current_le + 1 if current_le < len(sorted_questions) else 1
    prev_le = current_le - 1 if current_le > 1 else len(sorted_questions)

    try:
        titles = json.loads(current_question.title)
        desc = json.loads(current_question.descarray)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON in question data")

    if len(titles) != len(desc):
        return HttpResponseBadRequest("Title and descarray lengths do not match")

    options = dict(zip(titles, desc))

    question_numbers = [[(i * 10) + j + 1 for j in range(10)] for i in range(10)]
    next_questions_url = reverse('car:next_questions')

    request.session['current_le'] = current_le

    context = {
        'question': current_question,
        'question_answer': current_question.answer,
        'options': options,
        'current_le': current_le,
        'total_questions': len(sorted_questions),
        'next_le': next_le,
        'prev_le': prev_le,
        'question_numbers': question_numbers,
        'next_questions_url': next_questions_url,
        'question_url': current_question.url,
        'skill_explain': current_question.skillexplain,
    }

    return render(request, 'pk.html', context)
def forum(request):
    posts = post.objects.all()
    data_list = Comment.objects.all()
    if request.method == "GET":
        return render(request, 'forum.html', {'posts': posts,"data_list":data_list})
    content = request.POST.get("comment_text")
    current_datetime = datetime.datetime.now()
    post_id = request.POST.get("post_id")
    Post = get_object_or_404(post, id=post_id)
    Comment.objects.create(content=content,created_at=current_datetime,user_id=1,post=Post)
    return redirect('car:forum')

def chapter1(request):
    return redirect('car:show_chapter1', question_id=1)


def chapter2(request):
    return redirect('car:show_chapter2', question_id=68)
def show_chapter(request):
    return render(request, 'chapter.html')


def show_chapter(request):
    return render(request, 'chapter.html')


def show_chapter1(request, question_id):
    id_min = 1
    id_max = 67
    # 检查当前问题是否在指定范围内
    if not (id_min <= question_id <= id_max):
        raise Http404("Question not found within the specified range.")

    current_question = get_object_or_404(Question, pk=question_id)
    titles = json.loads(current_question.title)
    descriptions = json.loads(current_question.descarray)
    answer = current_question.answer
    if len(titles) != len(descriptions):
        raise ValueError("Title and descarray lengths do not match")

    paired_options = dict(zip(titles, descriptions))

    try:
        previous_question = Question.objects.filter(Q(pk__lt=question_id) & Q(pk__gte=id_min)).order_by('-pk').first()
    except Question.DoesNotExist:
        previous_question = None

    try:
        next_question = Question.objects.filter(Q(pk__gt=question_id) & Q(pk__lte=id_max)).order_by('pk').first()
    except Question.DoesNotExist:
        next_question = None

    context = {
        'question': current_question,
        'paired_options': paired_options,
        'previous_question': previous_question,
        'next_question': next_question,
        'answer': answer,
        'id_max': id_max
    }
    return render(request, 'chapter_1se.html', context)


def show_chapter2(request, question_id):
    id_min = 68
    id_max = 99
    # 检查当前问题是否在指定范围内
    if not (id_min <= question_id <= id_max):
        raise Http404("Question not found within the specified range.")
    current_question = get_object_or_404(Question, pk=question_id)
    titles = json.loads(current_question.title)
    descriptions = json.loads(current_question.descarray)
    answer = current_question.answer
    if len(titles) != len(descriptions):
        raise ValueError("Title and descarray lengths do not match")

    paired_options = dict(zip(titles, descriptions))

    try:
        previous_question = Question.objects.filter(Q(pk__lt=question_id) & Q(pk__gte=id_min)).order_by('-pk').first()
    except Question.DoesNotExist:
        previous_question = None

    try:
        next_question = Question.objects.filter(Q(pk__gt=question_id) & Q(pk__lte=id_max)).order_by('pk').first()
    except Question.DoesNotExist:
        next_question = None

    context = {
        'question': current_question,
        'paired_options': paired_options,
        'previous_question': previous_question,
        'next_question': next_question,
        'answer': answer,
        'id_max': id_max
    }
    return render(request, 'chapter_2se.html', context)


def show_chapterRa(request):
    last_question_id = request.session.get('last_question_id', None)
    # 获取ID在1到67之间的问题对象
    questions = Question.objects.filter(id__gte=1, id__lte=67)
    if questions.exists():
        if last_question_id:
            try:
                last_question = questions.get(id=last_question_id)
                questions = questions.exclude(id=last_question_id)
            except Question.DoesNotExist:
                pass

        random_question = random.choice(questions)
        request.session['last_question_id'] = random_question.id
        titles = json.loads(random_question.title)
        desc = json.loads(random_question.descarray)
        answer = random_question.answer
        if len(titles) != len(desc):
            raise ValueError("Title and descarray lengths do not match")

        options = dict(zip(titles, desc))

        # 构造上下文
        context = {
            'question_id': random_question.id,
            'question_title': random_question.title,
            'options': options,
            'correct_answer': answer,
            'question_question': random_question.question,
            'question_url': random_question.url,
            'skill_explain': random_question.skillexplain,
        }

        # 渲染模板
        return render(request, 'chapter_ra.html', context)
    else:
        raise Http404("No questions available within the specified range.")

def add_post(request):
    if request.method == "GET":
        return render(request,'create_post.html')
    title = request.POST.get("title")
    content = request.POST.get("content")
    username = request.session.get('username')
    post.objects.create(title=title,content=content,author=username)
    return redirect("car:forum")