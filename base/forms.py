from django.forms import ModelForm,ValidationError,ModelChoiceField,Form
from .models import Entry,Month,fileModel

class MonthForm(ModelForm):
    class Meta:
        model = Month
        fields = ['name','description']

class fileForm(ModelForm):
    class Meta:
        model = fileModel
        fields = ['file']

        def clean_file(self):
            file = self.cleaned_data.get('file')
            if file:
                if not file.name.endswith('.txt','.pdf'):
                    raise ValidationError("Only .txt files are allowed.")
            return file
        
class entryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['description']

class MonthComparisonForm(Form):
    month1 = ModelChoiceField(queryset=Month.objects.all(), required=True, label="Mes 1:")
    month2 = ModelChoiceField(queryset=Month.objects.all(), required=True, label="Mes 2:")