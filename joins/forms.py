from django import forms

from .models import Join

# class EmailForm(forms.Form):
# 	name = forms.CharField(required = False)
# 	email = forms.EmailField()


# Here, I have used a Model Form (one of Django's awesome features) which allows us
# to sit back while Django takes care of the form requirements by relating to the model
# we provide. Here it is the Join model.
class JoinForm(forms.ModelForm):
	class Meta:
		model = Join
		fields = ["email",]