from datetime import date
from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
import openpyxl
from rangefilter.filter import DateRangeFilter

from .forms import XLSXImportForm
from .models import *

# Register your models here.


class NutrientInline(admin.StackedInline):
    model = Nutrient


class TableAdmin(admin.ModelAdmin):
    model = Table
    search_fields = ['date', 'dietary_composition']
    change_list_template = 'admin/tables/Table/change_list.html'
    # summernote_fields = ('recipe',)
    inlines = [NutrientInline]
    list_filter = (
        ('date', DateRangeFilter),
    )

    # XLSX 파일을 Import 하여 실행할 기능을 정의한다.
    # Import XLSX
    def import_xlsx(self, request):
        if request.method == "POST":
            file = request.FILES.get('xlsx_file')
            initial_year = int(request.POST.get('date_input_year'))
            initial_month = int(request.POST.get('date_input_month'))

            # reader = csv.reader(csv_file)
            xlsx_file = openpyxl.load_workbook(file)
            nut_sheet = xlsx_file['Nutrition_Sheet']
            des_sheet = xlsx_file['Description_Sheet']
            entry_list = ['전체', '아침', '점심', '저녁', '간식']

            all_meal_list = list(nut_sheet.iter_rows())
            all_meal_des_list = list(des_sheet.iter_rows())

            # find non blank last row of the nut_sheet
            last_row = 0
            for cell in list(nut_sheet.columns)[0]:
                if cell.value is None:
                    last_row = cell.row
                    break

            bookmark = 1
            for i in range((last_row - 1)//5):
                for mark, entry in enumerate(entry_list, start=bookmark):
                    # Table Create
                    des_index = mark - (i + 1)
                    if entry is not '전체':
                        composition = all_meal_des_list[des_index][3].value.split(',')
                        table, nop = Table.objects.get_or_create(
                            dietary_composition=composition,
                            ingredients=all_meal_des_list[des_index][4].value,
                            recipe=all_meal_des_list[des_index][5].value,
                            tips=all_meal_des_list[des_index][6].value,
                            date=date(
                                initial_year,
                                initial_month,
                                i+1
                            ),
                            time=entry
                        )
                        # Table Nutrients Create
                        nut = table.nutrient
                        nut.calorie = all_meal_list[mark][3].value
                        nut.carbs = all_meal_list[mark][4].value
                        nut.fiber = all_meal_list[mark][5].value
                        nut.V_protein = all_meal_list[mark][6].value
                        nut.A_protein = all_meal_list[mark][7].value
                        nut.V_fat = all_meal_list[mark][8].value
                        nut.A_fat = all_meal_list[mark][9].value
                        nut.cholesterol = all_meal_list[mark][10].value
                        nut.salt = all_meal_list[mark][11].value
                        nut.potassium = all_meal_list[mark][12].value
                        nut.phosphorus = all_meal_list[mark][13].value
                        nut.V_calcium = all_meal_list[mark][14].value
                        nut.A_calcium = all_meal_list[mark][15].value
                        nut.V_iron = all_meal_list[mark][16].value
                        nut.A_iron = all_meal_list[mark][17].value

                        table.save()
                        nut.save()
                    bookmark += 1

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


class TableLogAdmin(admin.ModelAdmin):
    model = TableLog
    change_list_template = 'admin/tables/TableLog/change_list.html'
    search_fields = [
        'user__username', 'user__name', 'date'
    ]
    list_display = ['user', 'date', 'time']
    list_filter = (
        ('date', DateRangeFilter),
    )


admin.site.register(Table, TableAdmin)
admin.site.register(TableLog, TableLogAdmin)