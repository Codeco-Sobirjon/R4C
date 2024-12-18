from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    # Customize the list display to show important information about orders
    list_display = ('id', 'customer', 'robot_serial', 'quantity', 'created')
    # Make the customer and robot_serial searchable
    search_fields = ('customer__username', 'robot_serial__name')  # Assuming Robot model has a 'name' field
    # Enable filtering by customer and robot_serial
    list_filter = ('customer', 'robot_serial')
    # Enable ordering by the 'created' field
    ordering = ['created']
    # Display the number of orders in the admin dashboard
    list_per_page = 20  # You can adjust this to your preferred number

admin.site.register(Order, OrderAdmin)
