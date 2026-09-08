from django.db import models


class Course(models.Model):
    """A top-level course, e.g. BCA, B.Tech/B.E., B.Voc."""
    name = models.CharField(max_length=100)          # e.g. "BCA"
    degree = models.CharField(max_length=100)         # e.g. "Bachelor of Computer Applications"
    duration = models.CharField(max_length=50)        # e.g. "3 Years"
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Branch(models.Model):
    """A specialization/branch under a course (mainly used for B.Tech/B.E. and B.Voc)."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.course.name})"


class Fee(models.Model):
    """Fee amount for a course, tagged with the academic year."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    additional_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    academic_year = models.CharField(max_length=20, default='2026-27')  # e.g. "2026-27"

    def __str__(self):
        return f"{self.course.name} - Rs.{self.amount} ({self.academic_year})"


class FAQ(models.Model):
    """A ready-made question/answer pair used for questions that aren't
    course/fee lookups (e.g. eligibility, admission process, facilities)."""
    question = models.CharField(max_length=300)
    answer = models.TextField()
    intent = models.CharField(max_length=50)  # e.g. "eligibility", "admission"

    def __str__(self):
        return self.question


class Facility(models.Model):
    """Campus facility, e.g. Library, Sports, Hostel."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    """Contact details for the college / a department."""
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.department


class ChatMessage(models.Model):
    """Log of every question asked to the chatbot and the answer it gave.
    Useful to show in the viva as proof the chatbot is actually being used
    and to demonstrate the database in action."""
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_message[:50]} -> {self.bot_response[:50]}"
