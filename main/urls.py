from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test", views.Test, name="test"),
    path("login/", views.LoginView, name="login"),
    path("logout/", views.LogoutView, name="logout"),
    path("person/", views.ListPerson, name="list_person"),
    path("person/<int:person_id>/", views.ViewPerson, name="view_person"),
    path("person/edit/<int:person_id>/", views.EditPerson, name="edit_person"),
    path("person/new/", views.NewPerson, name="new_person"),
    path("invoice/", views.ListInvoice, name="list_invoice"),
    path("invoice/new", views.NewInvoice, name="new_invoice"),
    path("invoice/edit/<int:invoice_id>", views.EditInvoice, name="edit_invoice"),
    path("invoice/<int:invoice_id>", views.ViewInvoice, name="view_invoice"),
    path("payment/", views.ListSale, name="list_sale"),
    path("payment/<int:sale_id>", views.ViewSale, name="view_sale"),
    path("payment/new", views.NewSale, name="new_sale"),
    path("payment/edit/<int:sale_id>", views.EditSale, name="edit_sale"),
    path("schedule/", views.ScheduleList, name="schedule_list"),
    path("schedule/new", views.CreateSchedule, name="new_schedule"),
    path("schedule/<int:schedule_id>", views.EditSchedule, name="edit_schedule"),
    path("schedule/<int:schedule_id>/", views.DeleteSchedule, name="delete_schedule")
]