from django.db import models

# Create your models here.


class FNI(models.Model):
    class Meta:
        verbose_name = '식품영양성분'
        verbose_name_plural = f'{verbose_name} 목록'

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


# 건강기능식품 개별인정형 정보
class HFI(models.Model):
    class Meta:
        verbose_name = '건강기능식품 개별인정형 정보'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self.material_name}'

    material_name = models.CharField(blank=True, null=True, max_length=100, verbose_name='원료명')
    material_number = models.CharField(blank=True, null=True, max_length=50, verbose_name='원료 인정번호')
    daily_limit = models.CharField(blank=True, null=True, max_length=30, verbose_name='1일 섭취량 상한선')
    feature = models.TextField(blank=True, null=True, verbose_name='주요 기능성')
    caution = models.TextField(blank=True, null=True, verbose_name='섭취 주의사항')