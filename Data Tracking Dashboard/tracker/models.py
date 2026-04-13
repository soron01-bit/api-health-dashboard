from django.db import models


class DataEntry(models.Model):
	class Status(models.TextChoices):
		PENDING = 'pending', 'Pending'
		COMPLETE = 'complete', 'Complete'
		BLOCKED = 'blocked', 'Blocked'

	date = models.DateField()
	title = models.CharField(max_length=120)
	category = models.CharField(max_length=80)
	value = models.DecimalField(max_digits=12, decimal_places=2)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-date', '-created_at']

	def __str__(self):
		return f"{self.title} ({self.category})"
