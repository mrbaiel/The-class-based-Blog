from django import forms

from apps.blog.models import Post


class PostCreateForm(forms.ModelForm):
    """
    Форма для создания блогов на сайте
    """

    class Meta:
        model = Post
        fields = ('title', 'category', 'description', 'text', 'thumbnail', 'status')

    def __init__(self, *args, **kwargs):
        """
        форма для создания
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class PostUpdateForm(PostCreateForm):
    class Meta:
        model = Post
        fields = PostCreateForm().Meta.fields + ('updater', 'fixed')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fixed'].widget.attrs.update({
            'class': 'form-check-input'
        })