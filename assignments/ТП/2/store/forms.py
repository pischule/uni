from django import forms
from .models import ProductInstance, Product


class SellerCreateProductInstanceForm(forms.ModelForm):
    class Meta:
        model = ProductInstance
        fields = ['product', 'count']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SellerCreateProductInstanceForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(seller=user)
