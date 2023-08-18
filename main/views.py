from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import authenticate, login, logout, get_backends
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.contrib.auth.models import User
from reportlab.lib.pagesizes import letter
from django.core import serializers
from reportlab.pdfgen import canvas
from django.urls import reverse
from xhtml2pdf import pisa
from .functions import *
from .models import *


def createRecurringInvoice(inv_pk):
    recurring_time = Invoice.objects.get(pk=inv_pk).recurring_time
    inv = Invoice.objects.get(pk=inv_pk)
    for i in range(0, inv.recurring_qtd):
        inv_ = inv
        inv_.pk = None
        inv_.recurring_qtd -= 1
        print(inv_.release_date)
        inv_.release_date = inv_.release_date + datetime.timedelta(days=inv_.recurring_time)
        inv_.payment_date = inv_.payment_date + datetime.timedelta(days=inv_.recurring_time)

        inv_.save()
        inv=inv_

    return

def get_or_none(classmodel, classmodel_id):
     try:
         return classmodel.objects.get(pk=classmodel_id)
     except:
         return None

def user_is_staff(user):
    return user.groups.filter(name='Financeiro').exists() or user.is_superuser

def TesteContrato(request, sale_id):

    return render(request, 'contrato.html', {"sale":Sale.objects.get(pk=sale_id), "user":request.user})

def Test(request):
    account = Account.objects.all()

    context = {
        "account" : account
    }
    
    return render(request, "html/test.html", context)

def LoginView(request):
    context = {}
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect(reverse('index'))

        else:
            context = {
                "perms":request.user.get_all_permissions(),
                "username" : request.user,
                "error_message" : "Nome de usuário e/ou senha incorretos." 
            }

    return render(request, "html/login.html", context)

def LogoutView(request):
    logout(request)
    return redirect(reverse('login'))


@login_required(login_url="/login/")
def index(request):
    context={
        "perms":request.user.get_all_permissions(),
        "username":request.user
    }
    
    return render(request, "html/index.html", context)

@login_required(login_url="/login/")
def ListPerson(request):
    person = Person.objects.all()

    context = {
        "perms":request.user.get_all_permissions(),
        "username" : request.user,
        "person":person,
        }

    return render(request, "html/list_person.html", context)

@login_required(login_url="/login/")
def ViewPerson(request, person_id):
    if request.method=="POST":
        print(request.POST)
        person=Person.objects.get(pk=request.POST.get("pk"))
        print("deletou:\n")
        print(person)
        person.delete()

        return ListPerson(request)

    person = get_object_or_404(Person, pk=person_id)
    gender_list = Gender.objects.all().order_by('-pk')

    context = {
        "perms":request.user.get_all_permissions(),
        "username" : request.user,
        "person" : person,
        "gender_list":gender_list
    }

    return render(request, "html/view_person.html", context)

@login_required(login_url="/login/")
def EditPerson(request, person_id):
    if request.method=="POST":
        person = Person.objects.get(pk=request.POST.get('pk'))

        person.name = request.POST.get('name')
        person.cpf = request.POST.get('cpf')
        person.birth_date = request.POST.get('birth_date')
        person.gender = Gender.objects.get(pk=request.POST.get('gender')) 
        person.phone = request.POST.get('phone')
        person.cellphone = request.POST.get('cellphone')
        person.email = request.POST.get('email')
        person.cep = request.POST.get('cep')
        person.address = request.POST.get('address')
        person.city = request.POST.get('city')
        person.district = request.POST.get('district')
        # person.unit = get_or_none(Unit, request.POST.get('unit'))
        person.UF = request.POST.get('UF')
        person.complement = request.POST.get('complement')

        person.save()
        return redirect(reverse('view_person', args=[person_id]))

    person = get_object_or_404(Person, pk=person_id)
    gender_list = Gender.objects.all().order_by('-pk')

    context = {
        "perms":request.user.get_all_permissions(),
        "username" : request.user,
        "person" : person,
        "gender_list":gender_list
    }

    return render(request, "html/edit_person.html", context)

@login_required(login_url="/login/")
def NewPerson(request):
    if request.method=="POST":
        print(request.POST)
        p = Person(
            name = request.POST.get("name"),
            cpf = request.POST.get("cpf"),
            birth_date = request.POST.get("birth_date"),
            gender = Gender.objects.get(pk=request.POST.get("gender")),
            phone = request.POST.get("phone"),
            cellphone = request.POST.get("cellphone"),
            email = request.POST.get("email"),
            cep = request.POST.get("cep"),
            address = request.POST.get("address"),
            city = request.POST.get("city"),
            district = request.POST.get("district"),
            UF = request.POST.get("UF"),
            complement = request.POST.get("complement")
        )
        p.save()
        return redirect(reverse('list_person'))


    # unit_list = Unit.objects.all()
    # uf_list = UF
    gender_list = Gender.objects.all()

    context = {
        "perms":request.user.get_all_permissions(),
        "username" : request.user,
        # "uf_list" : uf_list,
        "gender_list" : gender_list
    }
    return render(request, "html/new_person.html", context)

@login_required(login_url="/login/")
@user_passes_test(user_is_staff, login_url="login")
def ListInvoice(request):
    invoice_list = Invoice.objects.all()

    context = {
        "perms":request.user.get_all_permissions(),
        "username" : request.user,
        "invoice_list" : invoice_list
    }

    return render(request, "html/list_invoice.html", context)

@login_required(login_url="/login/")
@user_passes_test(user_is_staff, login_url="login")
def ViewInvoice(request, invoice_id):
    if request.method == "POST":
        print("apagou")
        print(request.POST)
        invoice = Invoice.objects.get(pk=invoice_id)
        print(invoice)
        invoice.delete()

        return redirect(reverse('list_invoice'))


    invoice = Invoice.objects.get(pk=invoice_id)

    time = ""
    if invoice.recurring_time == '7':
        time = "Semanal"
    elif invoice.recurring_time == '15':
        time = "Quinzenal"
    elif invoice.recurring_time == '30':
        time = "Mensal"

    paid = ""
    if invoice.paid == True:
        paid = "Sim"
    else:
        paid = "Não"

    recurring = ""
    if invoice.recurring == True:
        recurring = "Sim"
    else:
        recurring = "Não"
        
    context = {
        "perms":request.user.get_all_permissions(),
        "username" : request.user,
        "invoice" : invoice,
        "time" : time,
        "paid" : paid,
        "recurring" : recurring,

    }
    return render(request, "html/view_invoice.html", context)


@login_required(login_url="/login/")
@user_passes_test(user_is_staff, login_url="login")
def NewInvoice(request):
    if request.method == "POST":
        print(request.POST)
        i = Invoice(
            invoice_type = get_or_none(Account, request.POST.get("invoice_type")), 
            supplier=get_or_none(Supplier, request.POST.get("supplier")),
            # unit = get_or_none(Unit, request.POST.get("unit")), 
            # payment_type = get_or_none(PaymentType, request.POST.get("payment_type")), 
            description = request.POST.get("description"), 
            release_date = request.POST.get("release_date"), 
            payment_date = request.POST.get("payment_date"), 
            cost = request.POST.get("cost"),
            recurring = eval(request.POST.get("recurring")), 
            recurring_qtd = int(request.POST.get("recurring_qtd")), 
            recurring_time = int(request.POST.get("recurring_time")) if request.POST.get("recurring_time") else None, 
            obs = request.POST.get("obs")
        )
        i.save()

        if i.recurring:
            createRecurringInvoice(i.pk)

        return redirect(reverse('list_invoice'))

    invoice_type_list = Account.objects.all()
    supplier_list = Supplier.objects.all()
    payment_type_list = PaymentType.objects.all()

    context = {
        "perms":request.user.get_all_permissions(),
        "username" : request.user,
        "invoice_type_list" : invoice_type_list,
        "supplier_list" : supplier_list,
        "payment_type_list" : payment_type_list,
    }

    return render(request, "html/new_invoice.html", context)

@login_required(login_url="/login/")
@user_passes_test(user_is_staff, login_url="login")
def EditInvoice(request, invoice_id):
    if request.method == "POST":
        invoice = Invoice.objects.get(pk=invoice_id)
        invoice.invoice_type = get_or_none(Account, request.POST.get("invoice_type")), 
        # invoice.unit = get_or_none(Unit, request.POST.get("unit")), 
        invoice.payment_type = get_or_none(PaymentType, request.POST.get("payment_type")), 
        invoice.description = request.POST.get("description")
        invoice.release_date = request.POST.get("release_date")
        invoice.payment_date = request.POST.get("payment_date")
        invoice.cost = request.POST.get("cost")
        invoice.recurring = eval(request.POST.get("recurring"))
        invoice.recurring_qtd = int(request.POST.get("recurring_qtd"))
        invoice.recurring_time = int(request.POST.get("recurring_time")) if request.POST.get("recurring_time") else None
        invoice.obs = request.POST.get("obs")
        print(f"{invoice.__dict__}\n")
        invoice.save()

        return redirect(reverse('list_invoice'))

    invoice = Invoice.objects.get(pk=invoice_id)
    supplier_list = Supplier.objects.all()
    invoice_type_list = Account.objects.all()

    time = ""
    if invoice.recurring_time == '7':
        time = "Semanal"
    elif invoice.recurring_time == '15':
        time = "Quinzenal"
    elif invoice.recurring_time == '30':
        time = "Mensal"

    paid = ""
    if invoice.paid == True:
        paid = "Sim"
    else:
        paid = "Não"

    recurring = ""
    if invoice.recurring == True:
        recurring = "Sim"
    else:
        recurring = "Não"
        
    context = {
        "perms":request.user.get_all_permissions(),
        "username" : request.user,
        "invoice" : invoice,
        "time" : time,
        "paid" : paid,
        "recurring" : recurring,
        "supplier_list" : supplier_list,
        "invoice_type_list" : invoice_type_list,

    }
    return render(request, "html/edit_invoice.html", context)

@login_required(login_url="/login/")
@user_passes_test(user_is_staff, login_url="login")
def ListSale(request):
    sale_list = Sale.objects.all()
    context = {
        "perms":request.user.get_all_permissions(),
        "username" : request.user,
        "sale_list" : sale_list
    }

    return render(request, "html/list_sale.html", context)

@login_required(login_url="/login/")
@user_passes_test(user_is_staff, login_url="login")
def NewSale(request):
    if request.method == "POST":
        print(request.POST)
        value = ""
        if request.POST.get("sale_type") == "1":
            service_post_value = request.POST.get("plan")

        elif request.POST.get("sale_type") == "2":
            service_post_value = request.POST.get("service")

        else:
            service_post_value = request.POST.get("product")

        service_value = value[len(request.POST.get("sale_type")):]

        s = Sale(
            sale_type = get_or_none(SaleType, request.POST.get("sale_type")),
            client = get_or_none(Person, request.POST.get("client")),
            seller = get_or_none(Employee, request.POST.get("seller")),
            status = get_or_none(SaleStatus, request.POST.get("status")),
            payment_type = get_or_none(PaymentType, request.POST.get("payment_type")),
            service = get_or_none(Service, service_value),
            discount = request.POST.get("discount"),
            sessions = request.POST.get("sessions"),
            discount_is_percent = True if request.POST.get("discount") == "percent" else False,
            obs = request.POST.get("obs"),
            date = request.POST.get("date"),
            origin = get_or_none(SaleOrigin, request.POST.get("sale_origin")),
            final_price = request.POST.get("final_price")
        )
        print(s.__dict__)
        s.save()

        return redirect(reverse("list_sale"))


    client_list = Person.objects.all()
    sale_type_list = SaleType.objects.all()
    seller_list = Employee.objects.all()
    status_list = SaleStatus.objects.all()
    payment_type_list = PaymentType.objects.all()
    plan_list = SaleService.objects.filter(service_type__pk=1)
    service_list = SaleService.objects.filter(service_type__pk=2)
    product_list = SaleService.objects.filter(service_type__pk=3)
    origin_list = SaleOrigin.objects.all()
    tax_list = Tax.objects.all()
    tax_json = list(Tax.objects.all())

    context = {
        "perms":request.user.get_all_permissions(),
        "username" : request.user,
        "client_list" : client_list,
        "sale_type_list" : sale_type_list,
        "seller_list" : seller_list,
        "status_list" : status_list,
        "payment_type_list" : payment_type_list,
        "plan_list" : plan_list,
        "product_list" : product_list,
        "service_list" : service_list,
        "payment_type_list" : payment_type_list,
        "tax_list":tax_list,
        "origin_list":origin_list
    }
    return render(request, "html/new_sale.html", context)

@login_required(login_url="/login/")
@user_passes_test(user_is_staff, login_url="login")
def ViewSale(request, sale_id):
    if request.method == "POST":
        sale = Sale.objects.get(pk=request.POST.get("pk"))
        print("Apagou")
        print(sale.__dict__)
        sale.delete()
        return redirect(reverse('list_sale'))

    sale = Sale.objects.get(pk=sale_id)
    context = {
        "perms":request.user.get_all_permissions(),
        "username" : request.user,
        "sale" : sale
    }
    return render(request, "html/view_sale.html", context)

@login_required(login_url="/login/")
@user_passes_test(user_is_staff, login_url="login")
def EditSale(request, sale_id):
    if(request.method=="POST"):
        value = ""
        if request.POST.get("sale_type") == "1":
            service_post_value = request.POST.get("plan")

        elif request.POST.get("sale_type") == "2":
            service_post_value = request.POST.get("service")

        else:
            service_post_value = request.POST.get("product")

        service_value = value[len(request.POST.get("sale_type")):]
        
        s=Sale.objects.get(pk=sale_id)
        s.sale_type = get_or_none(SaleType, request.POST.get("sale_type"))
        s.client = get_or_none(Person, request.POST.get("client"))
        s.seller = get_or_none(Employee, request.POST.get("seller"))
        s.status = get_or_none(SaleStatus, request.POST.get("status"))
        s.payment_type = get_or_none(PaymentType, request.POST.get("payment_type"))
        s.service = get_or_none(Service, value)
        s.discount = request.POST.get("discount")
        s.sessions = request.POST.get("sessions")
        s.obs = request.POST.get("obs")
        s.date = request.POST.get("date")
        s.final_price = request.POST.get("final_price")
        print(s.__dict__)
        s.save()

        return redirect(reverse('list_sale'))

    sale=Sale.objects.get(pk=sale_id)
    client_list = Person.objects.all()
    sale_type_list = SaleType.objects.all()
    seller_list = Employee.objects.all()
    status_list = SaleStatus.objects.all()
    payment_type_list = PaymentType.objects.all()
    service_list = SaleService.objects.filter(service_type__pk=2)
    product_list = SaleService.objects.filter(service_type__pk=3)
    plan_list = SaleService.objects.filter(service_type__pk=1)

    context = {
        "perms":request.user.get_all_permissions(),
        "username" : request.user,
        "sale" : sale,
        "client_list" : client_list,
        "sale_type_list" : sale_type_list,
        "seller_list" : seller_list,
        "status_list" : status_list,
        "payment_type_list" : payment_type_list,
        "service_list" : service_list,
        "payment_type_list" : payment_type_list,
    }

    return render(request, "html/edit_sale.html", context)

@login_required(login_url="/login/")
def ScheduleList(request):
    status_list = SaleStatus.objects.all()
    professional_list = Employee.objects.all()
    client_list = Person.objects.all()
    service_list = SaleService.objects.all()
    equipment_list = Equipment.objects.all()
    event_list = list(ScheduleEvent.objects.all().values())

    context = {
        "status_list" : status_list,
        "professional_list" : professional_list,
        "client_list" : client_list,
        "service_list" : service_list,
        "equipment_list" : equipment_list,
        "event_list" : event_list,
        "username":request.user
    }

    return render(request, "html/list_schedule.html", context)

def CreateSchedule(request):
    if request.method == "POST":
        print("\n\n\n")
        print(request.POST)
        print("\n\n\n")
        schedule = ScheduleEvent(
            title = "Agendamento",
            professional = get_or_none(Employee, request.POST.get("professional")),
            client = get_or_none(Person, request.POST.get("client")),
            category = "default",
            date = request.POST.get("date"),
            start = request.POST.get("start"),
            end = request.POST.get("end"),
            status = get_or_none(SaleStatus, request.POST.get("status")),
            service = get_or_none(SaleService, request.POST.get("service")),
            sessions = request.POST.get("sessions"),
            room = request.POST.get("room"),
            equipment = get_or_none(Equipment, request.POST.get("equipment")),
            obs = request.POST.get("obs")
        )
        print(schedule.__dict__)
        schedule.save()

    return redirect(reverse('schedule_list'))

def EditSchedule(request, schedule_id):
    if request.method=="POST":
        print("\n\n\n")
        print(request.POST)
        print("\n\n\n")

        schedule=ScheduleEvent.objects.get(pk=schedule_id)

        schedule.professional = get_or_none(Employee, request.POST.get("professional"))
        schedule.client = get_or_none(Person, request.POST.get("client"))
        schedule.date = request.POST.get("date")
        schedule.start = request.POST.get("start")
        schedule.end = request.POST.get("end")
        schedule.status = get_or_none(SaleStatus, request.POST.get("status"))
        schedule.service = get_or_none(SaleService, request.POST.get("service"))
        schedule.sessions = request.POST.get("sessions")
        schedule.room = request.POST.get("room")
        schedule.equipment = get_or_none(Equipment, request.POST.get("equipment"))
        schedule.obs = request.POST.get("obs")

        schedule.save()
        
    return redirect(reverse('schedule_list'))

def DeleteSchedule(request, schedule_id):
    if request.method=="POST":
        print("\n\n\n")
        print(request.POST)
        print("\n\n\n")

        schedule=ScheduleEvent.objects.get(pk=schedule_id)
        schedule.delete()

    return redirect(reverse('schedule_list'))

def PayInvoiceGroup(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]')  # Recebe o array de IDs
        today = datetime.date.today()
        for idx in ids:
            try:
                i = Invoice.objects.get(pk=idx)
                i.paid = True
                i.payment_date = today

                i.save()
            except Invoice.DoesNotExist:
                pass  # Lidar com o caso de ID inválido
            
        response_data = {
            'success': True,
            'message': 'Contas marcadas como pagas com sucesso.'
        }
        return JsonResponse(response_data)

        
    response_data = {
        'error': 'Método não permitido'
    }
    return JsonResponse(response_data, status=405)