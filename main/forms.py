from django import forms

class PersonForm(forms.Form):
    name = forms.CharField(max_length=50)
    cpf = forms.CharField(max_length=14)
    birth_date = forms.DateField()
    gender = forms.ForeignKey("Gender", required=false)
    phone = forms.IntegerField()
    cellphone = forms.IntegerField()
    email = forms.EmailField(max_length=128)
    unit = forms.ForeignKey("Unit",)
    cep = forms.CharField(max_length=9, required=false)
    address = forms.CharField(max_length=30, required=false)
    city = forms.CharField(max_length=30, required=false)
    discrict = forms.CharField(max_length=30, required=false)
    UF = forms.CharField(max_length=30, required=false)
    complement = forms.CharField(max_length=30, required=false)