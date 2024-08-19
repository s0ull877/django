from django import forms
import re

class CreateOrderForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(choices=[
        ('0', False),
        ('1', True)
    ])
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(choices=[
        ('0', False),
        ('1', True)
    ])


    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]

        if not data.isdigit():
            raise forms.ValidationError('The phone number must contain only numbers!')
        
        pattern = re.compile(r'^7\d{10}$')
        if not pattern.match(data):
            raise forms.ValidationError('The phone number is invalid!')
        
        return data
    
    def clean_delivery_address(self):
        data = self.cleaned_data["delivery_address"]
        
        requires_delivery = self.cleaned_data['requires_delivery'] == '1'
        if requires_delivery and not data:
            raise forms.ValidationError('This field cannot be empty at this time!')

        # TODO handler coordinates with google maps api

        return data
    
    