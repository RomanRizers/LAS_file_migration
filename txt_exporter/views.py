from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection

def export_to_txt(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_name')
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

        data = '\n'.join(['\t'.join(map(str, row)) for row in rows])

        response = HttpResponse(data, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{table_name}.txt"'
        return response
    else:
        return render(request, 'error.html', {'message': 'Ошибка при экспорте'})
