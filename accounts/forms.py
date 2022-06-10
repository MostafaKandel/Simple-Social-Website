from dataclasses import field
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    class Meta:
        fields=('username','email','password1','password2')
        model= get_user_model()
    ## super(): function used to give access to the methods of a parent class. return a temporary object of a parent class when used.

    # we using this only for customizing the label (not neccesary)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Dispaly Name'
        self.fields['email'].label="Email Address"