from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models

# Create your models here.
User = get_user_model()

# def Ingredient_validator()
# unique true option test
# if it doesn't work, use validator function


# class Ingredient(models.Model):
#     class Meta:
#         verbose_name = '식재료'
#         verbose_name_plural = f'{verbose_name} 목록'
#
#     def __str__(self):
#         return f'{self.name_list[0]}'
#
#     name_list = ArrayField(
#         models.CharField(max_length=10, blank=True, null=True),
#         blank=True, null=True, size=6, unique=True
#     )
#
#
# class Food(models.Model):
#     class Meta:
#         verbose_name = '음식'
#         verbose_name_plural = f'{verbose_name} 목록'
#
#     def __str__(self):
#         return f'{self.name}'
#
#     name = models.CharField(max_length=12, blank=True, unique=True)
#     ingredients = models.ManyToManyField(
#         Ingredient,
#         related_name='foods',
#         related_query_name='foods',
#         symmetrical=False
#     )


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
    # foods = models.ManyToManyField(
    #     Food,
    #     related_name='tables',
    #     related_query_name='tables',
    #     blank=True, null=True,
    #     verbose_name='음식 구성',
    #     symmetrical=False
    # )
    recipe = models.TextField(blank=True, null=True, verbose_name='레시피')
    nutrients = JSONField(blank=True, null=True)

    # def validate_unique(self, exclude=None):
    #     super(Table, self).validate_unique(exclude)
    #     if Table.objects.filter(foods=self.foods.all()).count() >= 1:
    #         raise ValidationError("이미 존재하는 식단입니다.")
    #     return True


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
    table = models.ForeignKey(Table, blank=True, null=True, verbose_name='섭취 식단')
    date = models.DateField(blank=True, null=True, auto_now_add=True, verbose_name='섭취 일자')
    time = models.CharField(
        max_length=8,
        choices=TABLE_TIME_CHOICES,
        blank=True,
        null=True,
        default='아침',
        verbose_name='섭취 시간'
    )