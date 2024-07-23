from django.shortcuts import render
from django.db import connection

def plot_graph(request):
    table_name = request.POST.get('table_name')
    print("Selected table name:", table_name)

    table_columns = []
    cursor = connection.cursor()
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s", [table_name])
    table_columns = [row[0] for row in cursor.fetchall() if row[0] != 'dept']

    query = "SELECT * FROM {}".format(connection.ops.quote_name(table_name))
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()

    context = {
        'selected_table_name': table_name,
        'selected_table_columns': table_columns,
        'rows': rows,
    }

    return render(request, 'graph.html', context)
