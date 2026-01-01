import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumni_project.settings') # Replace with your project name
django.setup()

from django.contrib.auth.models import User

# Configuration for your admin
username = "admin"
email = "admin@example.com"
password = "admin@123" # CHANGE THIS

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created successfully!")
else:
    print(f"Superuser '{username}' already exists.")
