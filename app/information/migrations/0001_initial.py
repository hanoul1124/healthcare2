# Generated by Django 2.2.5 on 2020-01-09 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FNI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='식품명')),
                ('food_group', models.CharField(blank=True, max_length=32, null=True, verbose_name='식품군')),
                ('food_amount', models.CharField(blank=True, max_length=8, null=True, verbose_name='1회 제공량(g)')),
                ('calorie', models.CharField(blank=True, max_length=8, null=True, verbose_name='열량(kcal)')),
                ('carbs', models.CharField(blank=True, max_length=8, null=True, verbose_name='탄수화물(g)')),
                ('protein', models.CharField(blank=True, max_length=8, null=True, verbose_name='단백질(g)')),
                ('fat', models.CharField(blank=True, max_length=8, null=True, verbose_name='지방(g)')),
                ('sugar', models.CharField(blank=True, max_length=8, null=True, verbose_name='당류(g)')),
                ('salt', models.CharField(blank=True, max_length=8, null=True, verbose_name='나트륨(mg')),
                ('cholesterol', models.CharField(blank=True, max_length=8, null=True, verbose_name='콜레스테롤(mg)')),
                ('saturated_fatty_acid', models.CharField(blank=True, max_length=8, null=True, verbose_name='포화지방산(g)')),
                ('trans_fat', models.CharField(blank=True, max_length=8, null=True, verbose_name='트랜스지방(g)')),
            ],
            options={
                'verbose_name': '식품영양성분',
                'verbose_name_plural': '식품영양성분 목록',
            },
        ),
        migrations.CreateModel(
            name='HFA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='원료명')),
                ('company', models.CharField(blank=True, max_length=30, null=True, verbose_name='회사명')),
                ('daily_intake', models.CharField(blank=True, max_length=150, null=True, verbose_name='1일 권 섭취량')),
                ('feature', models.TextField(blank=True, null=True, verbose_name='주요 기능성')),
                ('caution', models.TextField(blank=True, null=True, verbose_name='섭취 주의사항')),
            ],
            options={
                'verbose_name': '건강기능성식품 기능성 원료인정현황',
                'verbose_name_plural': '건강기능성식품 기능성 원료인정현황 목록',
            },
        ),
        migrations.CreateModel(
            name='HFC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='원료명')),
                ('ingredient', models.CharField(blank=True, max_length=30, null=True, verbose_name='성분명')),
                ('raw_daily_limit', models.CharField(blank=True, max_length=12, null=True, verbose_name='1일 섭취량 상한선')),
                ('limit_standard', models.CharField(blank=True, max_length=12, null=True, verbose_name='섭취량 단위')),
                ('feature', models.TextField(blank=True, null=True, verbose_name='주요 기능성')),
                ('caution', models.TextField(blank=True, null=True, verbose_name='섭취 주의사항')),
            ],
            options={
                'verbose_name': '건강기능성식품 품목 분류정보',
                'verbose_name_plural': '건강기능성식품 품목 분류정보 목록',
            },
        ),
        migrations.CreateModel(
            name='HFI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='원료명')),
                ('material_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='원료 인정번호')),
                ('daily_limit', models.CharField(blank=True, max_length=30, null=True, verbose_name='1일 섭취량 상한선')),
                ('feature', models.TextField(blank=True, null=True, verbose_name='주요 기능성')),
                ('caution', models.TextField(blank=True, null=True, verbose_name='섭취 주의사항')),
            ],
            options={
                'verbose_name': '건강기능식품 개별인정형 정보',
                'verbose_name_plural': '건강기능식품 개별인정형 정보 목록',
            },
        ),
    ]
