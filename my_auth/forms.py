from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from threading import Thread
from activation import send_activation

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="E-Mail")

    def save(self):
        user = super(RegisterForm, self).save(commit=False)
        user.is_active = False
        
        thread = Thread(target=send_activation, args=[user])
        thread.setDaemon(True)
        thread.start()

        user.save()

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError("A user with that email address already exists.")

    class Meta:
        model = User
        fields = ("username", "email",)