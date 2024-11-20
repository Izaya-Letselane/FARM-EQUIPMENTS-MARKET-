from django.contrib import admin
from .models import Customer, Product, Order, Profile
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)


#mix profile info and user info

class   ProfileInline(admin.StackedInline):
    model = Profile
    
#Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    field =["username", "first_name", "last_name", "email"]
    #to get everthing else
    inlines = [ProfileInline]
    
#Unregister the old way
admin.site.unregister(User)
#Re-register the user
admin.site.register(User, UserAdmin)