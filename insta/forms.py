from django import forms
from .models import Post, Chat, Reply, DMChat
from accounts.models import CustomUser

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'container'
            field.widget.attrs['class'] = 'item_1'

    class Meta:
        model = Post
        fields = ('image', 'caption')

class PostSearchForm(forms.Form):
    keyword = forms.CharField(label='キーワード', required=False)

class PostChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('comment', )

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields =('comment', )

class MyPageUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'bio', 'profile')

class DMChatForm(forms.ModelForm):
    class Meta:
        model = DMChat
        fields = ('text', )