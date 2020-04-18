from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.shortcuts import reverse
import itertools
from django.utils.text import slugify


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    post_title = models.CharField(max_length=200, null=False)
    post_content = models.TextField(default="My Content")
    date_published = models.DateField(blank=True, null=True,)
    user_profile_link = models.URLField(blank=True, null=True)
    img = models.ImageField(upload_to="img", null=True, blank=True)
    slug = models.SlugField(max_length=50)

    def get_blog_url(self):
        return reverse("home:blog", kwargs={'slug': self.slug})

    def _generate_slug(self):
        value = self.post_title
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Post.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()

        super().save(*args, **kwargs)

    @property
    def _get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def __str__(self):
        return self.post_title


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    post_title = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.username
