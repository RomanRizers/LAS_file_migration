from django.shortcuts import render
from django.http import JsonResponse
import psycopg2
from .utils import parse_las_file_and_insert_to_db

def upload_las_file(request):
    if request.method == 'POST' and request.FILES['las_file']:
        las_file = request.FILES['las_file']
        table_name = request.POST.get('table_name')
        if not las_file.name.endswith('.las'):
            return JsonResponse({'success': False})
        try:
            connection = psycopg2.connect(
                host="localhost",
                database="LASfile",
                user="postgres",
                password="1607"
            )

            parse_las_file_and_insert_to_db(las_file, connection, table_name)

            connection.close()
            return JsonResponse({'success': True})
        except psycopg2.Error as e:
            print("Ошибка при подключении к базе данных:", e)
            return JsonResponse({'success': False})
    return render(request, 'upload_las_file.html')

