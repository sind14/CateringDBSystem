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


class ClientNameSearchForm(forms.Form):
    client_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Name"}
        )
    )


class DishNameSearchForm(forms.Form):
    dish_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Name"}
        )
    )


class OrderSearchForm(forms.Form):
    client = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Name"}
        )
    )
