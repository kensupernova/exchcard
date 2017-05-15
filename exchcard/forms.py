#coding: utf-8

from django import forms

class UploadFileForm(forms.Form):
    """
    upload file form
    """
    title = forms.CharField(max_length=50)
    file = forms.FileField()

    def clean_message(self):
        message = self.cleaned_data['title']
        num_words = len(message.split())
        if num_words <= 0:
            raise forms.ValidationError("title is empty!")
        return message


class RegisterCardForm(forms.Form):
    """
    upload card photo form
    """
    card_name = forms.CharField(max_length=50)
    card_photo = forms.FileField()

    def clean_message(self):
        message = self.cleaned_data['card_name']
        num_words = len(message.split())
        if num_words < 0:
            raise forms.ValidationError("card name is empty")
        return message
