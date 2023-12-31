from django.db import models
from django.urls import reverse
from datetime import date
# Import the User
from django.contrib.auth.models import User

class Budget(models.Model):
  amount=models.DecimalField(max_digits=10, decimal_places=2)
  start_date=models.DateField('Start date')
  end_date=models.DateField('End date')
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.amount} from {self.start_date} to {self.end_date}"
  
  def get_absolute_url(self):
    return reverse('index')
  
class Category(models.Model):
  title=models.CharField(max_length=50)
  icon=models.CharField(max_length=200, default='fa-dollar-sign')
  color=models.CharField(max_length=50, default='rgba(255, 99, 132, 0.7)')
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def get_absolute_url(self):
    return reverse('categories_detail', kwargs={"category_id": self.id})
  
  def __str__(self):
    return f"{self.title}"

class Expense(models.Model):
  title=models.CharField(max_length=50)
  amount=models.DecimalField(max_digits=10, decimal_places=2)
  date=models.DateField('Payment date')
  category=models.ForeignKey(Category, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.title} on {self.date}"
   
  def get_absolute_url(self):
      return reverse("index")
  

  class Meta:
    ordering = ['-date']




  
