from django.db import models
from accounts.models import Student

DEPARTMENT_CHOICES = [
    ('MBA', 'Master of Business Administration'),
    ('BBA', 'Bachelor of Business Administration'),
    ('BCOM', 'Bachelor of Commerce'),
    ('BCA', 'Bachelor of Computer Applications'),
    ('MCOM', 'Master of Commerce'),
]

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    department = models.CharField(
        max_length=5,
        choices=DEPARTMENT_CHOICES,
        null=True,
        blank=True,
        help_text="Target Department (Optional)"
    )
    image = models.ImageField(
        upload_to='events/',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.title} ({self.date.date()})"


class EventRegistration(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    department=models.CharField(
        max_length=5,
        choices=DEPARTMENT_CHOICES,
        null=True,
        blank=True,
        help_text="Student Department at Registration"
    )

    class Meta:
        unique_together = ('student', 'event')  # ✅ Prevent duplicate registration

    def __str__(self):
        return f"{self.student.register_number} → {self.event.title}"


class Feedback(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE,null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.register_number} - {self.event.title} ({self.rating}⭐)"
