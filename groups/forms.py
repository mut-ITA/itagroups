from django import forms

from groups.models import Group

class ERRORS(object):
    EMPTY_NAME = "O nome do grupo nao pode ser vazio"
    EMPTY_ALIAS = "O alias do grupo nao pode ser vazio"
    EMPTY_TAGS = "As tags do grupo nao pode ser vazias"


class GroupForm(forms.models.ModelForm):

    class Meta:
        model = Group
        fields = ('name', 'alias', 'tags', 'description')
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Entre o nome do grupo',
                'class': 'form-control input-medium',
            }),
            'alias': forms.fields.TextInput(attrs={
                'placeholder': 'Entre o alias do grupo',
                'class': 'form-control input-medium',
            }),
            'tags': forms.fields.TextInput(attrs={
                'placeholder': 'Entre as tags do grupo',
                'class': 'form-control input-medium',
            }),
            'description': forms.fields.TextInput(attrs={
                'placeholder': 'Entre a descricao do grupo',
                'class': 'form-control input-medium',
            }),
        }
        error_messages = {
            'name': {'required': ERRORS.EMPTY_NAME},
            'alias': {'required': ERRORS.EMPTY_ALIAS},
            'tags': {'required': ERRORS.EMPTY_TAGS},
        }
