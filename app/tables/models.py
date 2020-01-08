from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.cache import cache
from django.db import models
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone

User = get_user_model()

# unique true option test
# if it doesn't work, use validator function


class Table(models.Model):
    class Meta:
        verbose_name = '식단'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['date', 'pk']
        unique_together = ('date', 'time',)

    def __str__(self):
        return f'{self.date} {self.time}의 식단'

    TABLE_TIME_CHOICES = (
        ('아침', 'Breakfast'),
        ('점심', 'Launch'),
        ('저녁', 'Dinner'),
        ('간식', 'Snack'),
    )

    dietary_composition = ArrayField(
        models.CharField(max_length=20, blank=True, null=True, default=""),
        blank=True, null=True, size=8, verbose_name='식단 구성'
        # ,unique=True
    )

    # 필요한 재료량
    ingredients = models.TextField(blank=True, null=True, verbose_name='재료', default=" ")
    # 레시피
    recipe = models.TextField(blank=True, null=True, verbose_name='레시피', default=" ")
    # 레시피 팁
    tips = models.TextField(blank=True, null=True, verbose_name='레시피 팁', default=" ")

    date = models.DateField(db_index=True, blank=True, null=True, verbose_name='날짜')
    time = models.CharField(
        max_length=8,
        choices=TABLE_TIME_CHOICES,
        blank=True,
        null=True,
        default='아침',
        verbose_name='섭취 시간'
    )
    
    def save(self, *args, **kwargs):
        cache.delete('table_list')
        super(Table, self).save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        cache.delete('table_list')
        super(Table, self).delete(*args, **kwargs)


class Nutrient(models.Model):
    class Meta:
        verbose_name = '영양정보'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self.table} 영양정보'

    table = models.OneToOneField(Table, on_delete=models.CASCADE, primary_key=True, verbose_name='식단')
    calorie = models.FloatField(blank=True, null=True, default=0, verbose_name='칼로리')
    carbs = models.FloatField(blank=True, null=True, default=0, verbose_name='탄수화물')
    fiber = models.FloatField(blank=True, null=True, default=0, verbose_name='섬유질')
    V_protein = models.FloatField(blank=True, null=True, default=0, verbose_name='식물성 단백질')
    A_protein = models.FloatField(blank=True, null=True, default=0, verbose_name='동물성 단백질')
    V_fat = models.FloatField(blank=True, null=True, default=0, verbose_name='식물성 지방')
    A_fat = models.FloatField(blank=True, null=True, default=0, verbose_name='동물성 지방')
    cholesterol = models.FloatField(blank=True, null=True, default=0, verbose_name='콜레스테롤')
    salt = models.FloatField(blank=True, null=True, default=0, verbose_name='나트륨')
    potassium = models.FloatField(blank=True, null=True, default=0, verbose_name='칼륨')
    phosphorus = models.FloatField(blank=True, null=True, default=0, verbose_name='인')
    V_calcium = models.FloatField(blank=True, null=True, default=0, verbose_name='식물성 칼슘')
    A_calcium = models.FloatField(blank=True, null=True, default=0, verbose_name='동물성 칼슘')
    V_iron = models.FloatField(blank=True, null=True, default=0, verbose_name='식물성 철')
    A_iron = models.FloatField(blank=True, null=True, default=0, verbose_name='동물성 철')

    @receiver(post_save, sender=Table)
    def create_table_nutrient(sender, instance, created, **kwargs):
        if created:
            Nutrient.objects.create(table=instance)

    @receiver(post_save, sender=Table)
    def save_table_nutrient(sender, instance, **kwargs):
        instance.nutrient.save()


# unique_together > date & time
class TableLog(models.Model):
    class Meta:
        verbose_name = '섭취 기록'
        verbose_name_plural = f'{verbose_name} 목록'
        unique_together = ('user', 'date', 'time',)
        ordering = ['date', 'pk']

    def __str__(self):
        return f'{self.pk}번 식단'

    TABLE_TIME_CHOICES = (
        ('아침', 'Breakfast'),
        ('점심', 'Launch'),
        ('저녁', 'Dinner'),
        ('간식', 'Snack'),
    )
    user = models.ForeignKey(User, db_index=True, blank=True, null=True, verbose_name='유저', on_delete=models.CASCADE)
    table = models.ForeignKey(Table, blank=True, null=True, verbose_name='섭취 식단', on_delete=models.CASCADE)
    date = models.DateField(blank=True, db_index=True, null=True, default=timezone.now, verbose_name='섭취 일자')
    time = models.CharField(
        max_length=8,
        choices=TABLE_TIME_CHOICES,
        blank=True,
        null=True,
        default='아침',
        verbose_name='섭취 시간'
    )
