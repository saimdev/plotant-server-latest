from django.db import models

class User(models.Model):
    google = models.IntegerField(null=True,  blank=True)
    github = models.IntegerField(null=True,  blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    plan = models.IntegerField(default=1) # 1 for basic, 2 for standard, 3 for premium
    project_create = models.IntegerField(default=0) #5 and 10
    add_files = models.IntegerField(default=0) # 3 and full
    file_size = models.IntegerField(default=5) # 25 and full
    multifields = models.CharField(max_length=255, default='bar')
    chart_plots = models.CharField(max_length=255, default='B, L, P')
    graph_limit = models.IntegerField(default=0) # 10 and full
    chart_download = models.CharField(max_length=255, default='J, J-PD-PN, A')
    shares = models.IntegerField(default=0) # 5 a
    account_create_date = models.DateField(null=True,  blank=True)
    plan_exp_date = models.DateField(null=True,  blank=True)


class Subscription(models.Model):
    plan_id = models.IntegerField(default=1)
    plan_name = models.CharField(max_length=255)
    project_create = models.IntegerField(default=1)  # 5 and 10
    add_files = models.IntegerField(default=2)  # 3 and 200
    file_size = models.IntegerField(default=5)  # 25 and 200
    multifields = models.CharField(max_length=255, default='bar')
    chart_plots = models.CharField(max_length=255, default='B,L,P')
    color_selection = models.BooleanField(default=0)
    custom_theme = models.BooleanField(default=0)
    graph_limit = models.IntegerField(default=3)  # 10 and 200
    logs = models.BooleanField(default=0)
    chart_download = models.CharField(max_length=255, default='J, J-PD-PN, A')
    shares = models.IntegerField(default=1)  # 5 and 10
    pdf_download = models.BooleanField(default=0)


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    holder_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16, unique=True)  
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4)
    

    