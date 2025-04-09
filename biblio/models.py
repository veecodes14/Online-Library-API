from django.db import models

class Biblio(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)

    def __str__(self):
        return self.title + ',' + ' ' + self.author

