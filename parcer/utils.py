import psycopg2
import lasio
import tempfile
import os
import numpy as np

def create_table(connection, column_names, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "{}" (
                id SERIAL PRIMARY KEY,
                {}
            )
        """.format(table_name.replace('"', '""'),
                   ", ".join('"{}" DECIMAL'.format(column_name.replace('"', '""'))
                             for column_name in column_names)))
        connection.commit()
    except psycopg2.Error as e:
        print("Ошибка при создании таблицы:", e)

def parse_las_file_and_insert_to_db(las_file, connection, table_name):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(las_file.read())
        temp_file_path = temp_file.name

    las = lasio.read(temp_file_path)

    column_names = las.keys()
    create_table(connection, column_names, table_name)

    data = zip(*[las[column_name] for column_name in column_names])

    cursor = connection.cursor()
    try:
        for row in data:
            if not np.isnan(row).any():
                cursor.execute("INSERT INTO {} ({}) VALUES ({})"
                               .format('"{}"'.format(table_name.replace('"', '""')),
                                       ','.join('"{}"'.format(col.replace('"', '""')) for col in column_names),
                                       ','.join(['%s'] * len(row))), row)
        connection.commit()
    except psycopg2.Error as e:
        print("Ошибка при добавлении данных в базу данных:", e)
    finally:
        cursor.close()

    os.remove(temp_file_path)

