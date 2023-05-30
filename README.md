1. トップページを作成する。ベーステンプレートのbase.htmlを作成し、それをextendsしたindex.htmlを作る。
　　generic.TemplateView使い、http://127.0.0.1:8000 で表示できるか確認する。

    ## urls.py
        
        from django.urls import path
        from . import views
        
        app_name = 'insta'
        
        urlpatterns = [
            path('', views.Top.as_view(), name='top'),
        ]

   ## views.py

         from django.views import generic
         
         class Top(generic.TemplateView):
             template_name = 'insta/index.html'
             model = Post

   ## base.html
        
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
            {% block content %}{% endblock %}
        </body>
        </html>

   ## index.html
        
        {% extends 'base.html' %}
         
        {% block content %}
        <h3>top</h3>
        
        {% endfor%}
        
        {% endblock %}

2. 主役となるモデルを実際に作ります。
   python manage.py makemigrationsとpython manage.py migrateをする。

   ## models.py
    
        class Post(models.Model):
            user = models.ForeignKey(User, on_delete=models.CASCADE)
            image = models.ImageField('画像')
            caption = models.TextField('説明')
        
            def __str__(self):
                return f'{self.user}-{self.caption[:10]}'

3. /admin/のDjango管理サイトから試しに何件か追加し、 ListViewを使ってトップページに表示する。

   ## views.py

         class Top(generic.ListView):
             template_name = 'insta/index.html'
             model = Post

   ## conf/settings.py

         MEDIA_ROOT = BASE_DIR/'media'
         
         MEDIA_URL = "/media/"

   ## conf/urls.py

         from django.conf.urls.static import static
         from django.conf import settings
         
         urlpatterns += static(
             settings.MEDIA_URL,
             document_root=settings.MEDIA_ROOT
         )

   ## index.html 追記

         {% for post in post_list %}
         <article>
             <h1>{{ post.user.username }}</h1>
             <img src="{{ post.image.url }}" />
             <p>{{ post.caption }}</p>
         </article>
         
         {% endfor%}

4. CreateViewを使って、主役となるモデルの作成ページを作っていきます。
　　保存したデータが、一覧や詳細ページで表示されることを確認しましょう。

   ## urls.py
   
       path('post/', views.PostCreate.as_view(), name='post_create'),

   ## views.py 

         from django.urls import reverse_lazy
         from .models import Post
         from .forms import PostForm
         
         class PostCreate(generic.CreateView):
             model = Post
             form_class = PostForm
             template_name = 'insta/post_create.html'
             success_url = reverse_lazy('insta:top')

   ## forms.py
   
         from django import forms
         from .models import Post
         
         class PostForm(forms.ModelForm):
             class Meta:
                 model = Post
                 fields = ('user', 'image', 'caption')

5. アカウント名を選択する画面を消して、連携できるようにする。

   ## views.py

         class PostCreate(generic.CreateView):

             def form_valid(self, form):
                 post = form.save(commit=False)
                 post.user = self.request.user
                 post.save()
         
                 return redirect('insta:top')

6. トップページから投稿画面に飛べるようにする

   ## template_file

         <p><a href="{% url 'insta:top' %}">BACK</a></p>

7. マイページを作る

   ## mypage.html

         {% extends 'base.html' %}
         
         {% block content %}
         <h1>{{ user.username }}</h1>
         
         <hr>
         
         <article>
         
         {% for post in post_list %}
             <img src="{{ post.image.url }}" />
         {% endfor %}
         
         </article>
         
         <hr>
         
         <div><a href="{% url 'insta:post_create' %}">POST</a></div>
         <div><a href="{% url 'insta:top' %}">TOP</a></div>
         
         {% endblock %}

   ## views.py

         class MyPage(generic.ListView):
             model = Post
             template_name = 'insta/mypage.html'
             form_class = PostForm
         
             def get_queryset(self):
                 queryset = Post.objects.all()
         
                 queryset = queryset.filter(user=self.request.user)
                 return queryset

8. 削除画面を作る 

   ## urls.py

       path('delete/<int:pk>/', login_required(views.PostDelete.as_view()), name='post_delete'),

   ## views.py

         class PostDelete(generic.DeleteView):
             model = Post
             template_name = 'insta/post_delete.html'
             success_url = reverse_lazy('insta:top')

   ## post_delete.html

         {% extends 'base.html' %}
          
         {% block content %}
         <form method="post">{% csrf_token %}
             <p>"{{ object }}"を削除してもよろしいですか?</p>
             <input type="submit" value="DELETE">
         </form>
         
         <hr>
         <div>
             <a href="{% url 'insta:top' %}">TOP</a>
         </div>
          
         {% endblock %}

   ## リンク元ファイル

         <div><a href="{% url 'insta:post_delete' post.id %}">DELETE</a></div>

9. ユーザーごとの投稿詳細画面を作る 

   ## urls.py

         path('my/post/', login_required(views.UserPost.as_view()), name='my_post'),

   ## views.py

         class UserPost(generic.ListView):
             model = Post
             template_name = 'insta/mypost.html'
         
             def get_queryset(self):
                 queryset = Post.objects.all()
         
                 queryset = queryset.filter(user=self.request.user)
                 return queryset

   ## mypost.html

         {% extends 'base.html' %}
          
         {% block content %}
         
         <div><a href="{% url 'insta:my_page' %}">BACK</a></div>
         <h3>{{ user.username }}</h3>
         <h2>投稿</h2>
         
         {% for post in post_list %}
         <article>
             <h4>@{{ post.user.username }}</h4>
             <img src="{{ post.image.url }}" />
             <p>{{ post.caption }}</p>
             <div><a href="{% url 'insta:post_delete' post.id %}">DELETE</a></div>
         </article>
         {% endfor %}
         
         {% endblock %}

10. アカウント作成画面を作る

11. CSSファイルを付与

STATIC_URL = 'static/'

STATICFILES_DIRS = [BASE_DIR / 'static']

class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'input'