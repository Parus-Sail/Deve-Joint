from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.create_superuser('admin', 'admin@mail.ru', 'pass')
user.email_verify = True
user.save()
