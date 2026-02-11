from django.db import models


class Student(models.Model):
    LEVEL_CHOICES = (
        ("ND I", "ND I"),
        ("ND II", "ND II"),
        ("ND III", "ND III"),
        ("HND I", "HND I"),
        ("HND II", "HND II"),
        ("HND III", "HND III"),
    )
    SEX_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    matric = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    has_voted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.matric})"
