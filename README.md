# LAS file migration

<p align="center">
  <img src="screenshots/main_page.png" alt="main" width="100%" height="100%" />
</p>

## Оглавление

- [Описание](#описание)
- [LAS формат](#LASформат)
- [Стек технологий](#Стек-технологий)
- [Функции WEB-сервиса](#Функции-WEB-сервиса)
- [UX/UI дизайн](#UX/UI-дизайн)
- [Реализация управления таблицами в базе данных](#реализация-управления-таблицами-в-базе-данных)
- [Экспорт данных](#экспорт-данных)
- [Скриншоты](#скриншоты)
- [Контейнизация с Docker](#контейнеризация-с-docker)


## Описание
Работа выполнена в рамках бакалаврской дипломной работы по теме: "Создание WEB-сервиса для миграции данных c использованием программ для электронных таблиц и СУБД".

Актуальность темы заключается в том, что WEB-сервис может быть использован в различных компаниях, занимающихся обработкой и анализом геофизических данных.
Внедрение такого инструмента позволит значительно сократить время и усилия, затрачиваемые на миграцию данных, повысить качество и точность анализа,
а также обеспечить интеграцию данных с другими информационными системами.

## LAS формат
LAS (Log ASCII Standard) файл — формат файла, используемый в нефтяной и газовой промышленности для хранения данных каротажных исследований скважин.
Данный формат основан в виде ASCII, то есть обычного текста, поэтому файлы могут быть открыты в любом, даже самом простом, текстовом редакторе.

В данный формат включаются следующие секции:
- `~V: секция «Version»`: обозначение версии файла LAS;
- `~W: секция «Well»`: перечисление идентификаторов скважины;
- `~C: секция «Curve»`: описывание кривых;
- `~P: секция «Parameters»`: описание параметров скважины;
- `~A: Секция «ASCII log data»`: хранение информации по кривым.

Пример LAS файла: 
<p align="center">
  <img src="Screenshots/LAS.png" alt="LAS" width="50%" height="50%" />
</p>


## Стек технологий

- Python 
- Django
- PostgreSQL
- HTML
- CSS
- JavaScript
- Figma
- Xlsx, TXT, JSON (в качестве экспорта данных)

## Функции WEB-сервиса
Основные функции WEB-сервиса:
<p align="center">
  <img src="screenshots/functions.png" alt="functions" />
</p>


## UX/UI дизайн
На стадии проектирования дизайн включал в себя семь основных элементов: 
- Главная страница
- Список таблиц
- Вывод таблицы
- График
- Подтверждение об успешном добавлении данных
- Изменение названия таблицы
- Подтверждение удаления

Немаловажным аспектом является создание связей между фреймами.
Они обеспечивают логичную и интуитивно понятную навигацию по WEB-сервису:
<p align="center">
  <img src="Screenshots/figma.png" alt="figma" width="100%" height="100%" />
</p>


## Реализация управления таблицами в базе данных
Для отображения списка таблиц используется функция list_tables. Она отвечает за получение списка всех таблиц, находящихся в базе данных,
за исключением системных и служебных таблиц Django. Для этого используется SQL-запрос к информации схемы базы данных.

Функция list_tables:
```python
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
```
Для отображения содержимого таблицы используется функция table_view.
Эта функция выполняет SQL-запрос для получения всех данных из указанной таблицы и передает их в HTML шаблон.

Функция table_view:
```python
def table_view(request, table_name):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM \"{}\"".format(table_name))
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    return render(request, 'table_view.html',
                  {'table_name': table_name,
                   'column_names': column_names, 'rows': rows})
```
Для переименования таблицы используется функция rename_table. Эта функция также обрабатывает POST-запрос и выполняет SQL-команду для переименования.
Функция принимает старое и новое имя таблицы и выполняет команду ALTER TABLE для переименования.

Функция rename_table:
```python
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
```
Для удаления таблицы используется функция delete_table. 
Эта функция обрабатывает POST-запрос, выполняет SQL-команду для удаления указанной таблицы и перенаправляет пользователя на страницу со списком таблиц.

Функция delete_table:
```python
def delete_table(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_name')
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS {}"
                       .format(connection.ops.quote_name(table_name)))
        cursor.close()
        return HttpResponseRedirect(reverse('list_tables'))
```
