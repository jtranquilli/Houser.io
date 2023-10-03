from django.db import models

# Create your models here.
# whenever we edit this file we need to do the command 'python manage.py makemigrations main' in terminal at the outer folder called 'mysite'
class ToDoList(models.Model):
    name = models.CharField(max_length=200)
    
    
    def __str__(self):
        return self.name

class HousingListing(models.Model):
    post_text = models.TextField(primary_key=True)
    price = models.FloatField()
    number_of_rooms = models.IntegerField()
    image_url  =models.TextField()
    post_id = models.TextField()
    user_id = models.TextField()
    address = models.TextField()
    time = models.TextField()

class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()
    
    def __str__(self):
        return self.name
    
    
    
