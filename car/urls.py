from django.urls import path
from . import views
app_name = 'car'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('keyi/',views.keyi,name='keyi'),
    path('keer/',views.keer,name='keer'),
    path('kesan/',views.kesan,name='kesan'),
    path('kesi/',views.kesi,name='kesi'),
    path('sequential/',views.sequential_view,name='sequential'),
    path('question/<int:question_id>/', views.show_question, name='show_question'),
    path('question/<int:question_id>/answer/', views.submit_answer, name='submit_answer'),
    path('question/<int:pk>/', views.show_question, name='question_detail'),
    path('chapter/<int:chapter_id>/', views.show_chapter, name='show_chapter'),
    path('random/', views.random_question, name='random_question'),
    path('next/', views.next_question, name='next_question'),
    path('previous/', views.previous_question, name='previous_question'),
    path('exam/', views.start_exam, name='exam_questions'),
    path('exam/previous/', views.previous_questions, name='previous_questions'),
    path('exam/previous/', views.previous_questions, name='next_questions'),
    path('pk/',views.pk, name='pk'),
    path('forum/', views.forum, name='forum'),
    path('add_post/', views.add_post, name='add_post'),
    path('chapter/', views.show_chapter, name='show_chapter'),
    path('chapter1_se1/', views.chapter1, name='chapter_se1'),
    path('chapter1_se2/', views.chapter2, name='chapter_se2'),
    path('chapterRa/', views.show_chapterRa, name='show_chapterRa'),
    path('chapter1/<int:question_id>/', views.show_chapter1, name='show_chapter1'),
    path('chapter2/<int:question_id>/', views.show_chapter2, name='show_chapter2'),
    ]
