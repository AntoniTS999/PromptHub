from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from prompthub import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Author(AbstractUser):
    display_name = models.CharField(max_length=100,
                                    blank=True,
                                    null=True,
                                    unique=True)

    def get_display_name(self):
        return self.display_name or self.username

    def __str__(self):
        return self.display_name or self.username

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ("username",)


class Prompt(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True,
                                   blank=True)
    categories = models.ManyToManyField(Category,
                                        related_name="prompts",
                                        blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="prompts",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        date_format = "%m/%d/%Y %H:%M:%S"
        created_at = self.created_at.strftime(date_format)
        updated_at = self.updated_at.strftime(date_format)
        preview = self.content[:25]
        return (f"{self.title} "
                f"| {self.author} "
                f"| {created_at} "
                f"| {updated_at} "
                f"| {preview}")

    def get_absolute_url(self):
        return reverse("prompts:prompt-detail", kwargs={"pk": self.id})

    class Meta:
        verbose_name = "Prompt"
        verbose_name_plural = "Prompts"
        ordering = ("-created_at",)


class Rating(models.Model):
    VALUE_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )
    value = models.IntegerField(choices=VALUE_CHOICES)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="ratings",
        on_delete=models.CASCADE
    )
    prompt = models.ForeignKey(Prompt,
                               related_name="ratings",
                               on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "prompt")

    def __str__(self):
        return str(self.value)


class Comment(models.Model):
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="comments",
        on_delete=models.CASCADE
    )
    prompt = models.ForeignKey(
        Prompt, related_name="comments",
        on_delete=models.CASCADE
    )

    def __str__(self):
        date_format = "%m/%d/%Y %I:%M %p"
        created_at = self.created_at.strftime(date_format)
        return f"{self.user} | {created_at}/: {self.content[:25]}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ("-created_at",)
