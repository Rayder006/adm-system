# from .models import Invoice, Supplier, InvoiceType
# import datetime

#def get_or_none(classmodel, classmodel_id):
#     try:
#         return classmodel.objects.get(pk=classmodel_id)
#     except classmodel.DoesNotExist:
#         return None

# def createRecurringInvoice(inv_pk):
#     recurring_time = Invoice.objects.get(pk=inv_pk).recurring_time
#     inv = Invoice.objects.get(pk=inv_pk)
#     for i in range(0, inv.recurring_qtd):
#         inv_ = inv
#         inv_.pk = None
#         inv_.recurring_qtd -= 1
#         print(inv_.release_date)
#         inv_.release_date = inv_.release_date + datetime.timedelta(days=inv_.recurring_time)
#         inv_.payment_date = inv_.payment_date + datetime.timedelta(days=inv_.recurring_time)

#         inv_.save()
#         inv=inv_

#     return