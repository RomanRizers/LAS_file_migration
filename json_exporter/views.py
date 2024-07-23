import json
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection

def export_to_json(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_name')
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
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
