from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect, resolve_url
from django.db.models import Q
from .models import Post, Chat, Reply, DMChat, Tag
from .forms import PostForm, PostSearchForm, PostChatForm, ReplyForm, MyPageUpdateForm, DMChatForm
from accounts.models import CustomUser


class Top(generic.ListView):
    template_name = 'insta/index.html'
    model = Post
    paginate_by = 3

    def get_queryset(self):
        user_list = self.request.user.follow.all()
        post_list = Post.objects.filter(user__in=user_list)

        return post_list.order_by('-created_at')

class Like(generic.TemplateView):
    template_name = 'insta/index.html'
    model = Post

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        user = self.request.user
        likes = user.like

        if post in likes.all():
            likes.remove(post)
        else:
            likes.add(post)

        return redirect('insta:top')


class PostCreate(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'insta/post_create.html'
    success_url = reverse_lazy('insta:top')

    def form_valid(self, form):
        post = form.save(commit=False)

        post.user = self.request.user

        caption = post.caption
        caption_list = caption.split()
        print(caption_list)

        post.save()

        for tag in caption_list:
            if tag.startswith('#'):
                if Tag.objects.filter(name=tag).exists():
                    add_tag = Tag.objects.filter(name=tag).first()
                    post.tags.add(add_tag)

                else:
                    add_tag = Tag.objects.create(name=tag)
                    post.tags.add(add_tag)

        return redirect('insta:top')

class PostTags(generic.ListView):
    template_name = 'insta/index.html'
    model = Post
    paginate_by = 3

    def get_queryset(self):
        tag = Tag.objects.get(id=self.kwargs['pk'])
        post_list = Post.objects.filter(tags=tag)
        return post_list.order_by('-created_at')


class UserPage(generic.ListView):
    model = Post
    template_name = 'insta/user_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.get(pk=self.kwargs['pk'])
        context['user'] = user
        context['post_list'] = Post.objects.filter(user=user)

        return context

    def post(self, request, *args, **kwargs):
        target_user = CustomUser.objects.get(pk=kwargs['pk'])
        user = self.request.user
        follow_user = user.follow

        if target_user in follow_user.all():
            follow_user.remove(target_user)
        else:
            follow_user.add(target_user)

        followers = user.follower
        followers.add(target_user)

        return redirect('insta:user_page', pk=kwargs['pk'])

class PostDelete(generic.DeleteView):
    model = Post
    template_name = 'insta/post_delete.html'
    success_url = reverse_lazy('insta:top')

class PostChat(generic.CreateView):
    model = Chat
    template_name = 'insta/post_chat.html'
    form_class = PostChatForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs['pk'])
        context['post'] = post
        context['chat_list'] = Chat.objects.filter(post=post)

        return context

    def get_success_url(self):
        return resolve_url('insta:post_chat', pk=self.kwargs['pk'])

    def form_valid(self, form):
        chat = form.save(commit=False)
        chat.user = self.request.user
        chat.save()

        return redirect('insta:top')

class PostReply(generic.CreateView):
    model = Reply
    template_name = 'insta/post_reply.html'
    form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat = Chat.objects.get(pk=self.kwargs['pk'])
        context['chat'] = chat
        context['reply_list'] = Reply.objects.filter(target=chat)

        return context

    def form_valid(self, form):
        chat = Chat.objects.get(pk=self.kwargs['pk'])

        reply = form.save(commit=False)
        reply.user = self.request.user
        reply.target = chat
        reply.save()

        return redirect('insta:top')

    def get_success_url(self):
        return resolve_url('insta:post_reply', pk=self.kwargs['pk'])

class MyPage(generic.ListView):
    model = CustomUser
    template_name = 'insta/mypage.html'
    form_class = PostForm

    def get_queryset(self):
        queryset = Post.objects.order_by('-created_at')
        queryset = queryset.filter(user=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['follow_list'] = self.request.user.follow.all()
        context['follower_list'] = self.request.user.follower.all()

        return context

    def post(self, request, *args, **kwargs):
        post = Post.objects.get()

        user = self.request.user
        follow_user = user.follow

        follow_user.add(post)

        followers = user.follower
        followers.add(post)

        return redirect('insta:my_page')

class SearchList(generic.ListView):
    model = Post
    template_name = 'insta/search.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.all()
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(user__username__icontains=keyword) | Q(tags__name__icontains=keyword)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostSearchForm(self.request.GET)

        return context

class MyPageUpdate(generic.UpdateView):
    model = CustomUser
    form_class = MyPageUpdateForm
    template_name = 'insta/mypage_update.html'
    success_url = reverse_lazy('insta:my_page')

    def get_object(self):
        return self.request.user

class FollowUserList(generic.TemplateView):
    template_name = 'insta/follow_user_list.html'

    # def get_queryset(self):
    #     queryset = CustomUser.objects.all()
    #
    #     queryset = queryset.filter(from_user=self.request.user)
    #     return queryset

# class DMChatList(generic.ListView):
#     model = DMChat
#     template_name = 'insta/dm.html'
#
#     def get_queryset(self):
#         queryset = DMChat.objects.all()
#
#         queryset = queryset.filter(from_user=self.request.user)
#         return queryset

class DMChatList(generic.CreateView):
    model = DMChat
    template_name = 'insta/dm.html'
    form_class =DMChatForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target = CustomUser.objects.get(id=self.kwargs['pk'])
        context['dmchat_list'] = DMChat.objects.filter(
            Q(from_user=self.request.user, to_user=target) | Q(from_user=target, to_user=self.request.user)
        )

        return context

    def form_valid(self, form):
        message = form.save(commit=False)
        message.from_user = self.request.user
        message.to_user = CustomUser.objects.get(id=self.kwargs['pk'])

        message.save()

        return redirect('insta:follow_user')

    def get_success_url(self):
        return resolve_url('insta:dm', pk=self.kwargs['pk'])

class BookMark(generic.ListView):
    template_name = 'insta/bookmark.html'
    model = Post

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        user = self.request.user
        bookmarks = user.bookmark

        if post in bookmarks.all():
            bookmarks.remove(post)
        else:
            bookmarks.add(post)

        return redirect('insta:top')

    def get_queryset(self):
        queryset = self.request.user.bookmark.all().order_by('-created_at')
        return queryset