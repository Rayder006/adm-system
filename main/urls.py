from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test", views.Test, name="test"),
    path("contrato/<int:sale_id>", views.SaleContract, name="sale_contract"),
    path("contrato/cancel/<int:sale_id>", views.SaleContract, name="cancel_contract"),
    path("login/", views.LoginView, name="login"),
    path("logout/", views.LogoutView, name="logout"),
    path("person/", views.ListPerson, name="list_person"),
    path("person/<int:person_id>/", views.ViewPerson, name="view_person"),
    path("person/edit/<int:person_id>/", views.EditPerson, name="edit_person"),
    path("person/new/", views.NewPerson, name="new_person"),
    path("invoice/", views.ListInvoice, name="list_invoice"),
    path("invoice/new", views.NewInvoice, name="new_invoice"),
    path("invoice/pay", views.PayInvoiceGroup, name="pay_invoices"),
    path("invoice/edit/<int:invoice_id>", views.EditInvoice, name="edit_invoice"),
    path("invoice/<int:invoice_id>", views.ViewInvoice, name="view_invoice"),
    path("sale/", views.ListSale, name="list_sale"),
    path("sale/cancel/<int:sale_id>", views.CancelSale, name="cancel_sale"),
    path("sale/<int:sale_id>", views.ViewSale, name="view_sale"),
    path("sale/new", views.NewSale, name="new_sale"),
    path("sale/edit/<int:sale_id>", views.EditSale, name="edit_sale"),
    path("sale/saleServiceAjax/<int:type_id>", views.saleServiceAjax, name="sale_service_ajax"),
    path("schedule/", views.ScheduleList, name="schedule_list"),
    path("schedule/new", views.CreateSchedule, name="new_schedule"),
    path("schedule/<int:schedule_id>/", views.DeleteSchedule, name="delete_schedule"),
    path("schedule/service_filter/<person_id>", views.ServiceAjax, name="schedule_service_ajax"),
    path("schedule/confirm/", views.ConfirmScheduleAjax, name="confirm_ajax"),
    path("receivable/", views.ListReceivable, name="list_receivable"),
    path("receivable/pay", views.ReceiveInvoiceGroup, name="receive_invoice"),
]