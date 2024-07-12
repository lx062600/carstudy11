from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class Question(models.Model):
    id = models.AutoField(primary_key=True)
    answer = models.TextField()
    skill = models.CharField(max_length=255)
    skillexplain = models.TextField()
    descarray = models.TextField()
    title = models.CharField(max_length=255)
    question = models.TextField()
    remark = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    versionNo = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('car:question_detail', kwargs={'pk': self.pk})


class post(models.Model):
    objects = None
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(post, on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} on {self.post.title} - {self.content[:20]}'

    class Meta:
        ordering = ['-created_at']

class CustomUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # 假设密码字段使用明文存储（实际项目中应当使用哈希加密）

    def __str__(self):
        return self.username