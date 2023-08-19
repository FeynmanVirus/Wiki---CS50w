from django.forms import ModelForm, TextInput, Textarea
from encyclopedia.models import WForm

class CreateForm(ModelForm):
    class Meta:
        model = WForm
        fields = ('title', 'content')

        widgets={
            'title': TextInput(attrs={
                 'name': 'title',
                 'label': '',
                 'placeholder': 'Enter Title Here', 
                 'style': 'width: 80%; margin-top: 20px;',
            }),
            'content': Textarea(attrs={
                'name': 'content', 
                'placeholder': 'Type your content here',
                 'style': 'margin-top: 20px;'
            })
        }
    

class EditForm(ModelForm):
    class Meta:
        model = WForm
        fields = ('title', 'content')

        widgets={
            'title': TextInput(attrs={
                 'name': 'title',
                 'label': '',
                 'placeholder': 'Enter Title Here', 
                 'style': 'width: 80%; margin-top: 20px;',
            }),
            'content': Textarea(attrs={
                'name': 'content', 
                'placeholder': 'Type your content here',
                 'style': 'margin-top: 20px;'
            })
        }
    def fill(self, title, content):
        self.title = title
        self.content = content
        return [self.title]

