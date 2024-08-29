from django import forms
from .models import Menu, Dish


class MenuForm(forms.ModelForm):
    menu_dishes = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Menu
        fields = "__all__"
