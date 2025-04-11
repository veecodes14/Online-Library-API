from django.db import models

class Biblio(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    published_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    available = models.BooleanField(default=True)
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)

    

    def __str__(self):
        return self.title + ',' + ' ' + self.author

