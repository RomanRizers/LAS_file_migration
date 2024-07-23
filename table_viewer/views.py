# views.py

from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect
from django.urls import reverse

def list_tables(request):
    cursor = connection.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return render(request, 'list_tables.html', {'tables': tables})

def table_view(request, table_name):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM {}".format(table_name))
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    return render(request, 'table_view.html', {'table_name': table_name, 'column_names': column_names, 'rows': rows})

def delete_table(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_name')
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))
        cursor.close()
        return HttpResponseRedirect(reverse('list_tables'))
