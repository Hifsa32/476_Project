from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        
    
        fields = ['title', 'description', 'date_time', 'location', 'tag'] 
        
        # Use widgets to customize the HTML input fields (like adding placeholders)
        widgets = {
            # TextInput for the title
            'title': forms.TextInput(attrs={
                'placeholder': 'Optional Title...', 
                # Tailwind class for full width and styling
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'
            }),
            # Textarea for the main content
            'description': forms.Textarea(attrs={
                'placeholder': 'What is on your mind? Share something unfiltered...', 
                'rows': 8, # Make the box tall
                # Tailwind class for full width and styling
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg resize-y'
            }),
             'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
             'location': forms.TextInput(attrs={'placeholder': 'City, State/Country'}),
             'tag': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'
            }),
        }