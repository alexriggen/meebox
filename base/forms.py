from django.forms import ModelForm,ValidationError,ModelChoiceField,Form,forms,Select,TextInput,Textarea
from .models import Entry,Month,fileModel

class MonthForm(ModelForm):
    class Meta:
        model = Month
        fields = ['name', 'description']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Mes y año'}),
            'description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Detalles', 'rows': 4}),
        }
        labels = {
            'name': 'Month Name',
            'description': 'Month Description',
        }
    
    def __init__(self, *args, **kwargs):
        super(MonthForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Mes y año'
        self.fields['description'].label = 'Detalles'

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
        widgets = {
            'description': Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Detalles', 
                'rows': 4
            }),
        }
        labels = {
            'description': 'Detalles',
        }
    
    def __init__(self, *args, **kwargs):
        super(entryForm, self).__init__(*args, **kwargs)
        self.fields['description'].label = 'Detalles'

class MonthComparisonForm(Form):

    month1 = ModelChoiceField(
        queryset=Month.objects.all(), 
        required=True, 
        label="Mes 1:",
        widget=Select(attrs={'class': 'form-control'})
    )
    month2 = ModelChoiceField(
        queryset=Month.objects.all(), 
        required=True, 
        label="Mes 2:",
        widget=Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super(MonthComparisonForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'