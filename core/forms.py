from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Adınız")
    last_name = forms.CharField(max_length=30, required=True, label="Soyadınız")
    email = forms.EmailField(required=True, label="E-Posta Adresi")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        # Kullanıcı adını email'den üret (benzersiz ve küçük harf olsun)
        user.username = self.cleaned_data["email"].lower()
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
