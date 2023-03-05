from django.forms import ModelForm, CharField, TextInput, DateField, DateInput, Textarea
from .models import Tag, Author, Quote


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25,
                     required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, max_length=50,
                         required=True, widget=TextInput())
    description = CharField(min_length=3, max_length=1000,
                            required=False, widget=TextInput())
    born_date = DateField(
        input_formats=['%Y-%m-%d'], required=True, widget=DateInput)
    born_location = CharField(min_length=3, max_length=100,
                              required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'description', 'born_date', 'born_location']


class AuthorDetailForm(ModelForm):
    fullname = CharField(widget=Textarea())
    description = CharField(widget=Textarea())
    born_date = DateField(widget=Textarea())
    born_location = CharField(widget=Textarea())

    class Meta:
        model = Author
        fields = ['fullname', 'description', 'born_date', 'born_location']


class QuoteForm(ModelForm):
    quote = CharField(min_length=5, max_length=4000,
                      required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ['quote']
        exclude = ['tags', 'author']
