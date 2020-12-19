from django import forms

from .models import BlogPost


class BlogPostForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)


class BlogPostModelForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'slug', 'content', 'publish_date']


    def clean_title(self, *args, **kwargs):
        instance = self.instance
        title = self.cleaned_data.get('title')
        qs = BlogPost.objects.filter(title__iexact=title)
        if instance is not None: # if the instance is what we work on we don't want to raise validation error.
            qs = qs.exclude(pk=instance.pk) # id = instance.id
        if qs.exists():
            raise forms.ValidationError("This title has already been used. Please use other title.")
        return title