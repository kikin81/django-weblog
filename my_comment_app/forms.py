from django import forms
from django.contrib.comments.forms import CommentForm
from my_comment_app.models import CommentWithTitle
from francisco_utils import fields as francisco_utils

class CommentFormWithTitle(CommentForm):
    title = forms.CharField(max_length=300)
    recaptcha = francisco_utils.ReCaptchaField()

    def get_comment_model(self):
        # Use our custom comment model
        return CommentWithTitle

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
        data = super(CommentFormWithTitle, self).get_comment_create_data()
        data['title'] = self.cleaned_data['title']
        return data