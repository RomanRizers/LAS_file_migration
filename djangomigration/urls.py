from django.contrib import admin
from django.urls import path
from parcer.views import upload_las_file
from table_viewer import views
from export.views import export_to_excel
from export.views import export_to_json
from export.views import export_to_txt
from plots.views import plot_graph
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', upload_las_file, name='upload_las_file'),
    path('tables/', views.list_tables, name='list_tables'),
    path('tables/<str:table_name>/', views.table_view, name='table_view'),
    path('delete_table/', views.delete_table, name='delete_table'),
    path('export/', export_to_excel, name='export_to_excel'),
    path('export/json/', export_to_json, name='export_to_json'),
    path('txt/', export_to_txt, name='export_to_txt'),
    path('rename_table/', views.rename_table, name='rename_table'),
    path('plot/', plot_graph, name='plot_graph'),
    path('plot/<str:table_name>/', plot_graph, name='plot_graph'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
