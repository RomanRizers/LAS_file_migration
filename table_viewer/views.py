from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import connection

def list_tables(request):
    excluded_tables = [
        'django_migrations',
        'django_content_type',
        'auth_permission',
        'auth_group',
        'auth_group_permissions',
        'auth_user',
        'auth_user_groups',
        'auth_user_user_permissions',
        'django_admin_log',
        'django_session'
    ]

    cursor = connection.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = [row[0] for row in cursor.fetchall() if row[0] not in excluded_tables]
    cursor.close()

    return render(request, 'list_tables.html', {'tables': tables})


def table_view(request, table_name):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM \"{}\"".format(table_name))
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    return render(request, 'table_view.html',
                  {'table_name': table_name,
                   'column_names': column_names, 'rows': rows})


def delete_table(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_name')
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS {}"
                       .format(connection.ops.quote_name(table_name)))
        cursor.close()
        return HttpResponseRedirect(reverse('list_tables'))


def rename_table(request):
    if request.method == 'POST':
        old_table_name = request.POST.get('old_table_name')
        new_table_name = request.POST.get('new_table_name')

        cursor = connection.cursor()
        cursor.execute("ALTER TABLE {} RENAME TO {}".
                       format(connection.ops.quote_name(old_table_name),
                              connection.ops.quote_name(new_table_name)))
        cursor.close()

        return HttpResponseRedirect(reverse('list_tables'))

