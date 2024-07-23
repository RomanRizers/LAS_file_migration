import openpyxl
import json
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection

def export_to_excel(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_name')
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM {}".format(connection.ops.quote_name(table_name)))
            rows = cursor.fetchall()

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = table_name

        columns = [desc[0] for desc in cursor.description]
        ws.append(columns)

        for row in rows:
            ws.append(row)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{table_name}.xlsx"'
        wb.save(response)
        return response
    else:
        return HttpResponse('Ошибка при экспорте', status=405)


def export_to_json(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_name')
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM {}".format(connection.ops.quote_name(table_name)))
            rows = cursor.fetchall()

        def decimal_default(obj):
            if isinstance(obj, Decimal):
                return str(obj)
            raise TypeError

        data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        json_data = json.dumps(data, indent=4, default=decimal_default)

        response = HttpResponse(json_data, content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{table_name}.json"'
        return response
    else:
        return render(request, 'error.html', {'message': 'Метод не поддерживается'})


def export_to_txt(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_name')
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM {}".format(connection.ops.quote_name(table_name)))
            rows = cursor.fetchall()

        data = '\n'.join(['\t'.join(map(str, row)) for row in rows])

        response = HttpResponse(data, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{table_name}.txt"'
        return response
    else:
        return render(request, 'error.html', {'message': 'Ошибка при экспорте'})

