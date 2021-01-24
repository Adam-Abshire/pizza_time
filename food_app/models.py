from django.db import models
import re
from django.contrib import messages
import bcrypt

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must contain 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must contain 2 characters"
        if len(postData['pword']) < 8:
            errors['pword'] = "Password must contain 8 characters"
        if len(postData['address']) < 8:
            errors['address'] = "Address must contain 8 characters"
        if len(postData['city']) < 4:
            errors['city'] = "City must contain 4 characters"
        if len(postData['state']) < 2:
            errors['state'] = "State must contain 2 characters"
        if postData['pword'] != postData['pword_confirm']:
            errors['pword_confirm'] = "Passwords do not match"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = ("Invalid email address!")
        return errors

    def editval(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must contain 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must contain 2 characters"
        if len(postData['address']) < 8:
            errors['address'] = "Address must contain 8 characters"
        if len(postData['city']) < 4:
            errors['city'] = "City must contain 4 characters"
        if len(postData['state']) < 2:
            errors['state'] = "State must contain 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = ("Invalid email address!")
        return errors
    
    def loginval(self, postData):
        errors = {}
        all_users = User.objects.all()
        all_emails = []
        for user in all_users:
            all_emails.append(user.email)
        if postData['email'] not in all_emails:
            errors['email'] = "Email is not recognized, please register"
        
        if postData['email'] in all_emails:
            user = User.objects.filter(email= postData['email'])
            if bcrypt.checkpw(postData['pword'].encode(), user[0].password.encode()) == False:
                errors['pword'] = "Password is not correct"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Pizza(models.Model):
    method = models.CharField(max_length=25)
    size = models.CharField(max_length=125)
    crust = models.CharField(max_length=25)
    price = models.FloatField(default=14.99)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ordered_by = models.ForeignKey(User, related_name="pizzas_ordered", on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="liked_pizzas")

class Topping(models.Model):
    name = models.CharField(max_length=20, blank=True)
    pizzas_topped = models.ManyToManyField(Pizza, related_name="toppings", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)