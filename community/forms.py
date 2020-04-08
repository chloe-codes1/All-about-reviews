from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        label='Title',
        help_text='Your title must be no more than 100 characters in length',
        widget=forms.TextInput(
            attrs={
                'class':'my_input',
                'placeholder': "Give your review a headline"
            }
        )
    )
    
    movie_title = forms.CharField(
        max_length=30,
        help_text='Please type full movie title',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'ex) Before Sunrise'
            }
        )
    )

    content = forms.CharField(
        label='Content',
        min_length=30,
        help_text='30 Character minimum',
        widget=forms.Textarea(
            attrs={
                'row':5,
                'col':50,
                'placeholder': 'Write your review to help others learn about this movie'
            }
        )
    )

    rank = forms.IntegerField(
        label='Overall rating',
        help_text='Range from 0 to 5',
        widget=forms.NumberInput(
            attrs={
                'type':'range',
                'class': 'custom-range',
                'min': '0',
                'max' :'5',
            }
        )
    )
    class Meta:
        model = Review
        fields = '__all__'    