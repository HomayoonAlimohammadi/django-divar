from django.db import models


class Blog(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self) -> str:
        return f"Blog({self.name})"


class Author(models.Model):
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=200, null=True)
    email = models.EmailField()

    def __str__(self) -> str:
        return f"Author({self.name})"


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=128)
    description = models.TextField()
    pub_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)
    number_of_comments = models.IntegerField(default=0)
    number_of_likes = models.IntegerField(default=0)
    rating = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        ordering = ["-pub_date", "-number_of_likes"]

    def __str__(self) -> str:
        return f"Post({self.title})"
