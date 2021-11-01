from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path("", views.index, name="expenses"),
    path("search-expenses/", csrf_exempt(views.search_expenses), name="search_expenses"),
    path("add-expenses/", views.add_expenses_view, name='add_expenses'),
    path("edit-expenses/<int:id>", views.edit_expenses_view, name='edit_expenses'),
    path("delete-expenses/<int:id>", views.delete_expenses_view, name='delete_expenses')
]
