from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

User = get_user_model()

# unique true option test
# if it doesn't work, use validator function


class Table(models.Model):
    class Meta:
        verbose_name = '식단'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self.pk}번 식단'

    dietary_composition = ArrayField(
        models.CharField(max_length=20, blank=True, null=True),
        blank=True, null=True, size=8, unique=True, verbose_name='식단 구성'
    )

    recipe = models.TextField(blank=True, null=True, verbose_name='레시피')
    # nutrients = JSONField(blank=True, null=True)


class Nutrient(models.Model):
    class Meta:
        verbose_name = '영양정보'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self.table} 영양정보'

    table = models.OneToOneField(Table, on_delete=models.CASCADE, primary_key=True)
    calorie = models.PositiveSmallIntegerField(blank=True, null=True)
    carbs = models.PositiveSmallIntegerField(blank=True, null=True)
    fiber = models.PositiveSmallIntegerField(blank=True, null=True)
    A_protein = models.PositiveSmallIntegerField(blank=True, null=True)
    V_protein = models.PositiveSmallIntegerField(blank=True, null=True)
    A_fat = models.PositiveSmallIntegerField(blank=True, null=True)
    V_fat = models.PositiveSmallIntegerField(blank=True, null=True)
    cholesterol = models.PositiveSmallIntegerField(blank=True, null=True)
    salt = models.PositiveSmallIntegerField(blank=True, null=True)
    potassium = models.PositiveSmallIntegerField(blank=True, null=True)
    phosphorus = models.PositiveSmallIntegerField(blank=True, null=True)
    A_calcium = models.PositiveSmallIntegerField(blank=True, null=True)
    V_calcium = models.PositiveSmallIntegerField(blank=True, null=True)

    @receiver(post_save, sender=Table)
    def create_table_nutrient(sender, instance, created, **kwargs):
        if created:
            Nutrient.objects.create(table=instance)

    @receiver(post_save, sender=Table)
    def save_table_nutrient(sender, instance, **kwargs):
        instance.nutrient.save()


class TodayTable(models.Model):
    class Meta:
        verbose_name = '오늘의 식단'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self.date}의 식단'

    TABLE_TIME_CHOICES = (
        ('아침', 'Breakfast'),
        ('점심', 'Launch'),
        ('저녁', 'Dinner'),
        ('간식(오전)', 'Snack(AM)'),
        ('간식(오후)', 'Snack(PM)'),
    )
    table = models.ForeignKey(Table, blank=True, on_delete=models.CASCADE, verbose_name='식단')
    date = models.DateField(blank=True, null=True, verbose_name='날짜')
    time = models.CharField(
        max_length=8,
        choices=TABLE_TIME_CHOICES,
        blank=True,
        null=True,
        default='아침',
        verbose_name='섭취 시간'
    )


class TableLog(models.Model):
    class Meta:
        verbose_name = '오늘의 식단'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self.pk}번 식단'

    TABLE_TIME_CHOICES = (
        ('아침', 'Breakfast'),
        ('점심', 'Launch'),
        ('저녁', 'Dinner'),
        ('간식(오전)', 'Snack(AM)'),
        ('간식(오후)', 'Snack(PM)'),
    )
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='유저', on_delete=models.CASCADE)
    table = models.ForeignKey(Table, blank=True, null=True, verbose_name='섭취 식단', on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True, auto_now_add=True, verbose_name='섭취 일자')
    time = models.CharField(
        max_length=8,
        choices=TABLE_TIME_CHOICES,
        blank=True,
        null=True,
        default='아침',
        verbose_name='섭취 시간'
    )