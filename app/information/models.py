from django.db import models

# Create your models here.


class FNI(models.Model):
    class Meta:
        verbose_name = '식품영양성분 DB'
        verbose_name_plural = f'{verbose_name} 목록'
        # unique_together = ('user', 'date', 'time',)
        # ordering = ['date', 'pk']

    def __str__(self):
        return f'{self.food_name}'

    food_name = models.CharField(blank=True, null=True, max_length=100, verbose_name='식품명')
    food_group = models.CharField(blank=True, null=True, max_length=32, verbose_name='식품군')
    food_amount = models.CharField(blank=True, null=True, max_length=8, verbose_name='1회 제공량(g)')
    calorie = models.CharField(blank=True, null=True, max_length=8, verbose_name='열량(kcal)')
    carbs = models.CharField(blank=True, null=True, max_length=8, verbose_name='탄수화물(g)')
    protein = models.CharField(blank=True, null=True, max_length=8, verbose_name='단백질(g)')
    fat = models.CharField(blank=True, null=True, max_length=8, verbose_name='지방(g)')
    sugar = models.CharField(blank=True, null=True, max_length=8, verbose_name='당류(g)')
    salt = models.CharField(blank=True, null=True, max_length=8, verbose_name='나트륨(mg')
    cholesterol = models.CharField(blank=True, null=True, max_length=8, verbose_name='콜레스테롤(mg)')
    saturated_fatty_acid = models.CharField(blank=True, null=True, max_length=8, verbose_name='포화지방산(g)')
    trans_fat = models.CharField(blank=True, null=True, max_length=8, verbose_name='트랜스지방(g)')
