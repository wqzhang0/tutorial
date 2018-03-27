from django.db import models

# Create your models here.

class Persion(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    order = models.IntegerField(name='sql_order')

    class Meta:
        db_table = 'my_self_persion'
        ordering = ('-sql_order',)