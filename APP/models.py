from django.db import models


class User(models.Model):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        if not self.parent:
            return f"{self.name}"
        else:
            return f"{self.parent} --> {self.name}"

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    like = models.IntegerField(default=0)
    unlike = models.IntegerField(default=0)
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at', )

    def __str__(self):
        return f"{self.owner}-->{self.title}"



#