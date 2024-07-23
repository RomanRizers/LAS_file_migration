from django.http import HttpResponse
import openpyxl
from django.db import connection

def export_to_excel(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_name')
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
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
