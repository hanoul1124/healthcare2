import os
from datetime import date

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect
from django.urls import path
import openpyxl
from .forms import XLSXImportForm
from .models import *

# Register your models here.

class TableAdmin(admin.ModelAdmin):
    change_list_template = 'admin/tables/change_list.html'

    # XLSX 파일을 Import 하여 실행할 기능을 정의한다.
    # Import XLSX
    def import_xlsx(self, request):
        if request.method == "POST":
            file = request.FILES.get('xlsx_file')
            date_input = datetime.date(
                int(request.POST.get('date_input_year')),
                int(request.POST.get('date_input_month')),
                int(request.POST.get('date_input_day'))
            )
            # reader = csv.reader(csv_file)
            xlsx_file = openpyxl.load_workbook(file)
            worksheet = xlsx_file.active
            meal_list = []
            for i in range(1, worksheet.max_row + 1):
                cell = worksheet.cell(i, 1)
                if cell.value == '아침식사':
                    breakfast = i
                    meal_list.append(breakfast)
                elif cell.value == '점심식사':
                    launch = i
                    meal_list.append(launch)
                elif cell.value == '저녁식사':
                    dinner = i
                    meal_list.append(dinner)
                elif cell.value == '오전간식':
                    am_snack = i
                    meal_list.append(am_snack)
                elif cell.value == '오후간식':
                    pm_snack = i
                    meal_list.append(pm_snack)
                elif cell.value == '1일전체':
                    last = i
                    meal_list.append(last)

            breakfast_composition_list = [worksheet.cell(food, 2).value for food in range(breakfast, launch) if
                                          worksheet.cell(food, 2).value is not None]
            launch_composition_list = [worksheet.cell(food, 2).value for food in range(launch, dinner) if
                                       worksheet.cell(food, 2).value is not None]
            dinner_composition_list = [worksheet.cell(food, 2).value for food in range(dinner, am_snack) if
                                       worksheet.cell(food, 2).value is not None]
            am_snack_composition_list = [worksheet.cell(food, 2).value for food in range(am_snack, pm_snack) if
                                         worksheet.cell(food, 2).value is not None]
            pm_snack_composition_list = [worksheet.cell(food, 2).value for food in range(pm_snack, last) if
                                         worksheet.cell(food, 2).value is not None]

            br_table, br_created = Table.objects.get_or_create(dietary_composition=breakfast_composition_list)
            TodayTable.objects.create(table=br_table, date=date_input, time='아침')
            lc_table, lc_created = Table.objects.get_or_create(dietary_composition=launch_composition_list)
            TodayTable.objects.create(table=lc_table, date=date_input, time='점심')
            dn_table, dn_created = Table.objects.get_or_create(dietary_composition=dinner_composition_list)
            TodayTable.objects.create(table=dn_table, date=date_input, time='저녁')
            as_table, as_created = Table.objects.get_or_create(dietary_composition=am_snack_composition_list)
            TodayTable.objects.create(table=as_table, date=date_input, time='간식(오전)')
            ps_table, ps_created = Table.objects.get_or_create(dietary_composition=pm_snack_composition_list)
            TodayTable.objects.create(table=ps_table, date=date_input, time='간식(오후)')

            table_list = [br_table, lc_table,  dn_table, as_table, ps_table]

            nut_list = []
            for nut in range(4, worksheet.max_column + 1):
                cell = worksheet.cell(1, nut)
                if cell.value == '에너지(kcal)':
                    calorie = nut
                    nut_list.append(calorie)
                elif cell.value == '탄수화물(g)':
                    carbs = nut
                    nut_list.append(carbs)
                elif cell.value == '식물성 지질(g)':
                    V_fat = nut
                    nut_list.append(V_fat)
                elif cell.value == '동물성 지질(g)':
                    A_fat = nut
                    nut_list.append(A_fat)
                elif cell.value == '식물성 단백질(g)':
                    V_protein = nut
                    nut_list.append(V_protein)
                elif cell.value == '동물성 단백질(g)':
                    A_protein = nut
                    nut_list.append(A_protein)
                elif cell.value == '식이섬유(g)':
                    fiber = nut
                    nut_list.append(fiber)
                elif cell.value == '식물성 칼슘(mg)':
                    V_calcium = nut
                    nut_list.append(V_calcium)
                elif cell.value == '동물성 칼슘(mg)':
                    A_calcium = nut
                    nut_list.append(A_calcium)
                elif cell.value == '인(mg)':
                    phosphorus = nut
                    nut_list.append(phosphorus)
                elif cell.value == '나트륨(mg)':
                    salt = nut
                    nut_list.append(salt)
                elif cell.value == '칼륨(mg)':
                    potassium = nut
                    nut_list.append(potassium)
                elif cell.value == '콜레스테롤(mg)':
                    cholesterol = nut
                    nut_list.append(cholesterol)

            for index, table in enumerate(table_list):
                nutrient = table.nutrient
                nutrient.calorie = worksheet.cell(meal_list[index+1]-1, nut_list[0]).value
                nutrient.carbs = worksheet.cell(meal_list[index+1]-1, nut_list[1]).value
                nutrient.fiber = worksheet.cell(meal_list[index+1]-1, nut_list[2]).value
                nutrient.A_protein = worksheet.cell(meal_list[index+1]-1, nut_list[3]).value
                nutrient.V_protein = worksheet.cell(meal_list[index+1]-1, nut_list[4]).value
                nutrient.A_fat = worksheet.cell(meal_list[index+1]-1, nut_list[5]).value
                nutrient.V_fat = worksheet.cell(meal_list[index+1]-1, nut_list[6]).value
                nutrient.cholesterol = worksheet.cell(meal_list[index+1]-1, nut_list[7]).value
                nutrient.salt = worksheet.cell(meal_list[index+1]-1, nut_list[8]).value
                nutrient.potassium = worksheet.cell(meal_list[index+1]-1, nut_list[9]).value
                nutrient.phosphorus = worksheet.cell(meal_list[index+1]-1, nut_list[10]).value
                nutrient.A_calcium = worksheet.cell(meal_list[index+1]-1, nut_list[11]).value
                nutrient.V_calcium = worksheet.cell(meal_list[index+1]-1, nut_list[12]).value
                nutrient.save()
            return redirect("..")
        # XLSX file 제출용 HTML 페이지로 연결
        # 여기서 XLSX 파일을 업로드하면
        form = XLSXImportForm()
        return render(
            request, "admin/xlsx_form.html", {"form": form}
        )

    def get_urls(self):
        urls = super(TableAdmin, self).get_urls()
        new_urls = [
            path('import-xlsx/', self.import_xlsx),
        ] + urls
        return new_urls


    # Admin 사이트의 모든 URL을 가져오는 함수
    # 여기에 새롭게 추가할 기능의 url을 연결할 수 있게
    # path들로 이루어진 urls 리스트에 my_url을 추가한다.

# class CustomAdminSite(admin.AdminSite):
#     def get_urls(self):
#         urls = super(CustomAdminSite, self).get_urls()
#         new_urls = [
#             path('import-xlsx/', TableAdmin.import_xlsx),
#         ]
#         return urls + new_urls


admin.site.register(Table, TableAdmin)
admin.site.register(Nutrient)
admin.site.register(TodayTable)
