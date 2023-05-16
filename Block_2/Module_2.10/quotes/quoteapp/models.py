from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=25, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name='tag of username')
        ]

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    fullname = models.CharField(max_length=50, null=False, unique=True)
    description = models.CharField(max_length=1000, null=True, unique=False)
    born_date = models.DateField(null=False, unique=False)
    born_location = models.CharField(max_length=100, null=False, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'fullname'], name='author by username')
        ]

    def __str__(self):
        return f"{self.fullname}"


class Quote(models.Model):
    quote = models.TextField(max_length=4000, null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.quote}"
