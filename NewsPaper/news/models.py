from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm
from django import forms

# Create your models here.

class Author(models.Model):
    ratingAuthor = models.IntegerField(default = 0)
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):

        postRat = self.post_set.all().aggregate(ratingPost = Sum('ratingPost'))
        pRat = 0
        pRat += postRat.get('ratingPost')

        commentRat = self.authorUser.comment_set.all().aggregate(ratingComment = Sum('ratingComment'))
        cRat = 0
        cRat += commentRat.get('ratingComment')

        commentPostRat = Comment.objects.filter(commentPost__author = self).values('ratingComment').aggregate(ratingComment = Sum('ratingComment'))
        cPRat = 0
        cPRat += commentPostRat.get('ratingComment')

        # print('pRat =', pRat * 3, 'cRat = ', cRat, 'cPRat = ', cPRat)

        self.ratingAuthor = pRat * 3 + cRat + cPRat
        self.save()

class Category(models.Model):
    category = models.CharField(max_length = 255, unique = True)

class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    TYPE_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    type = models.CharField(max_length = 2, choices = TYPE_CHOICES, default = NEWS)
    timePost = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length = 255)
    textPost = models.TextField()
    ratingPost = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def like(self):
        self.ratingPost += 1
        self.save()

    def dislike(self):
        self.ratingPost -= 1
        self.save()

    def preview(self):
        return self.textPost[:124] + '...'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete = models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    textComment = models.TextField()
    timeComment = models.DateTimeField(auto_now_add=True)
    ratingComment = models.IntegerField(default=0)

    commentPost = models.ForeignKey(Post, on_delete = models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        try:
            return self.commentPost.author.authorUser.username
        except:
            return self.commentUser.username


    def like(self):
        self.ratingComment +=1
        self.save()

    def dislike(self):
        self.ratingComment -=1
        self.save()
        
class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")  # опционально
    last_name = forms.CharField(label="Фамилия")  # опционально

    class Meta:
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )


# Create your models here.