from django import forms
from myapp.models import Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['subject', 'intro_course', 'time', 'avg_age']
        widgets = {'time': forms.RadioSelect(), }
        labels = {'time': u'Preferred Time', 'avg_age': u'What is your age?', 'intro_course': u'This should be an introductory level course'}


class InterestForm(forms.Form):
    interested = forms.TypedChoiceField(widget=forms.RadioSelect, coerce=int, choices=((1, "Yes"), (0, "No")))
    age = forms.IntegerField(initial=20)
    comments = forms.CharField(widget=forms.Textarea, label='Additional Comments', required=False)
