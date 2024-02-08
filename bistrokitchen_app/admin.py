from django.contrib import admin
from bistrokitchen_app.models import menuitem, contact, chef, testimonial
# Register your models here.



# menuitem
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'details', 'category', 'is_active']
    list_filter = ['category', 'is_active']

admin.site.register(menuitem, MenuItemAdmin)

# contact
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'message']

admin.site.register(contact, ContactAdmin)

# chef
class ChefAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'position', 'chefdetails', 'chefimage']

admin.site.register(chef, ChefAdmin)

# Testimonials
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['id', 'testimony', 'pname', 'ptitle', 'ptimage']

admin.site.register(testimonial, TestimonialAdmin)