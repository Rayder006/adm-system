from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import authenticate, login, logout, get_backends
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.core import serializers
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from decimal import Decimal
from .functions import *
from .models import *


def createRecurringInvoice(inv_pk):
    inv = Invoice.objects.get(pk=inv_pk)
    recurring_time = Invoice.objects.get(pk=inv_pk).recurring_time
    
    for i in range(0, inv.recurring_qtd):
        inv_ = inv
        inv_.pk = None
        inv_.recurring_qtd -= 1
        print(inv_.release_date)
        inv_.release_date = inv_.release_date + datetime.timedelta(days=inv_.recurring_time)
        inv_.due_date = inv_.due_date + datetime.timedelta(days=inv_.recurring_time)

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

def SaleContract(request, sale_id):
    sale=Sale.objects.get(pk=sale_id)
    sale.status=SaleStatus.objects.get(pk=2)
    sale.save()
    if sale.sale_type.pk == 4:
        return render(request, 'contracts/contrato2.html', {"sale":sale, "user":request.user})
    else:
        return render(request, 'contracts/contrato1.html', {"sale":sale, "user":request.user})

def Test(request):
    sale=Sale.objects.get(pk=23)
    
    return render(request, 'contrato2.html', {"sale":sale, "user":request.user})

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
            cellphone = request.POST.get("cellphone"),
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
    invoice_list = Invoice.objects.filter(invoice_type__is_expense=True)

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
        cost = request.POST.get("cost")[3:].replace(".", "").replace(",", ".")
        i = Invoice(
            invoice_type = get_or_none(Account, request.POST.get("invoice_type")), 
            supplier=get_or_none(Supplier, request.POST.get("supplier")), 
            description = request.POST.get("description"), 
            release_date = request.POST.get("release_date"), 
            due_date = request.POST.get("due_date"),  #atenção !!
            cost = cost,
            recurring = eval(request.POST.get("recurring")), 
            recurring_qtd = int(request.POST.get("recurring_qtd")), 
            recurring_time = int(request.POST.get("recurring_time")) if request.POST.get("recurring_time") else None, 
            obs = request.POST.get("obs")
        )
        i.save()

        if i.recurring:
            createRecurringInvoice(i.pk)

        return redirect(reverse('list_invoice'))

    invoice_type_list = Account.objects.filter(is_expense=True)
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

    invoice = Invoice.objects.get(pk=invoice_id)
    if invoice.invoice_type.is_expense==False:
        return redirect(reverse("list_receivable"))

    if request.method == "POST":
        print("\n\n")
        print(request.POST)
        print("\n\n")
        invoice.invoice_type = get_or_none(Account, request.POST.get("invoice_type"))
        invoice.payment_type = get_or_none(PaymentType, request.POST.get("payment_type"))
        invoice.description = request.POST.get("description")
        invoice.release_date = request.POST.get("release_date")
        invoice.due_date = request.POST.get("due_date")
        invoice.cost = request.POST.get("cost")
        invoice.recurring = eval(request.POST.get("recurring"))
        invoice.recurring_qtd = int(request.POST.get("recurring_qtd"))
        invoice.recurring_time = int(request.POST.get("recurring_time")) if request.POST.get("recurring_time") else None
        invoice.obs = request.POST.get("obs")
        print(f"{invoice.__dict__}\n")
        invoice.save()

        return redirect(reverse('list_invoice'))

    supplier_list = Supplier.objects.all()
    invoice_type_list = Account.objects.filter(is_expense=True)

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

        service = SaleService.objects.get(pk=request.POST.get("service"))
        final_price = Decimal(request.POST.get("final_price"))
        discount = final_price
        discount -= service.price * service.sessions
        payment_type = get_or_none(PaymentType, request.POST.get("payment_type"))
        payment_type2 = None if request.POST.get("mixed") == 0 else get_or_none(PaymentType, request.POST.get("payment_type"))
        installments1=int(request.POST.get("installments1"))
        installments2=int(request.POST.get("installments1"))
        mixed = request.POST.get("mixed")==1
        price1 = Decimal(request.POST.get("price1"))
        price2 = Decimal(request.POST.get("price2")) if mixed==1 else None


        s = Sale(
            client = get_or_none(Person, request.POST.get("client")),
            seller = get_or_none(Employee, request.POST.get("seller")),
            status = SaleStatus.objects.get(pk=1), # novo
            origin = get_or_none(SaleOrigin, request.POST.get("origin")),
            service = service,
            payment_type = payment_type,
            payment_type2 = payment_type2,
            discount = discount,
            sessions = request.POST.get("sessions"),
            obs = request.POST.get("obs"),
            release_date = datetime.datetime.today(),
            counter = 0,
            price1 = price1,
            price2 = 0 if request.POST.get("mixed") == 0 else price2,
            installments1 = installments1,
            installments2 = 0 if request.POST.get("mixed") == 0 else installments2,
            final_price = final_price
        )

        s.save()
        s=Sale.objects.get(pk=s.id)
        print(s.__dict__)

        price1 /= installments1
        if mixed:
            price2 /= installments2


        if payment_type.has_tax:
            tax = Tax.objects.get(pk=request.POST.get("tax"))
            cost = (Decimal(request.POST.get("price1"))*(tax.tax/100))/installments1
            i = Invoice(
                invoice_type = Account.objects.get(pk=117) if payment_type.pk==1 else Account.objects.get(pk=118), # 117 == crédito; 118 == débito
                supplier = None,
                payment_type = payment_type,
                generator_sale = s,
                description = "Despesa Gerada Automáticamente",
                release_date = datetime.datetime.today(),
                due_date = datetime.datetime.today() + datetime.timedelta(days=int(30)),
                payment_date = None,
                cost = cost,
                paid = False,
                recurring = True,
                recurring_qtd = installments1-1,
                recurring_time = 30,
                obs = "Despesa Gerada Automáticamente"
            )

            i.save()
            price1-=cost
            createRecurringInvoice(i.pk)

        i = Invoice(
            invoice_type = s.service.account,
            supplier = None,
            payment_type = payment_type,
            generator_sale = s,
            description = "Receita Gerada Automáticamente",
            release_date = datetime.datetime.today(),
            due_date = datetime.datetime.today()+datetime.timedelta(days=30),
            payment_date = None,
            cost = price1,
            paid = False,
            recurring = True,
            recurring_qtd = installments1-1,
            recurring_time = 30,
            obs = "Receita Gerada Automáticamente"
        ) 
        i.save()

        createRecurringInvoice(i.pk)

        

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
    tax_list = list(Tax.objects.all().values())

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
    sale=Sale.objects.get(pk=sale_id)
    if sale.status.pk!=1:
        return redirect(reverse("list_sale"))

    if request.method=="POST":
        value = ""
        if request.POST.get("sale_type") == "1":
            service_post_value = request.POST.get("plan")

        elif request.POST.get("sale_type") == "2":
            service_post_value = request.POST.get("service")

        else:
            service_post_value = request.POST.get("product")

        service_value = value[len(request.POST.get("sale_type")):]
        
        sale=Sale.objects.get(pk=sale_id)
        sale.sale_type = get_or_none(SaleType, request.POST.get("sale_type"))
        sale.client = get_or_none(Person, request.POST.get("client"))
        sale.seller = get_or_none(Employee, request.POST.get("seller"))
        sale.status = SaleStatus.objects.get(pk=1)
        sale.payment_type = get_or_none(PaymentType, request.POST.get("payment_type"))
        sale.service = get_or_none(SaleService, value)
        sale.discount = request.POST.get("discount")
        sale.sessions = request.POST.get("sessions")
        sale.obs = request.POST.get("obs")
        sale.date = request.POST.get("date")
        sale.final_price = request.POST.get("final_price")
        print(sale.__dict__)
        sale.save()

        try:
            invoice = Invoice.object.get(generator_sale__id=s.id)
            console.log("invoice existe!")
            invoice.invoice_type = account
            invoice.supplier = None
            invoice.payment_type = None
            invoice.description = account.commentary
            invoice.release_date = datetime.datetime.today()
            invoice.payment_date = None
            invoice.cost = (Decimal(float(request.POST.get("final_price")))) * (tax.tax/100)
            invoice.paid = False
            invoice.recurring = False
            invoice.recurring_qtd = 0
            invoice.recurring_time = 0
            invoice.generator_sale = Sale.objects.get(pk=s.id)
            invoice.obs = "Despesa com cartão de débito" if tax.payment_type.pk ==  1 else "Despesa com cartão de crédito"
            console.log(invoice)
            invoice.save()
        except:
            pass 
            

        return redirect(reverse('list_sale'))

    client_list = Person.objects.all()
    sale_type_list = SaleType.objects.all()
    seller_list = Employee.objects.all()
    status_list = SaleStatus.objects.all()
    payment_type_list = PaymentType.objects.all()
    service_list = SaleService.objects.filter(service_type__pk=2)
    product_list = SaleService.objects.filter(service_type__pk=3)
    plan_list = SaleService.objects.filter(service_type__pk=1)
    origin_list = SaleOrigin.objects.all()

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
        "plan_list" : plan_list,
        "product_list" : product_list,
        "origin_list" : origin_list,
    }

    return render(request, "html/edit_sale.html", context)

@login_required(login_url="/login/")
def ScheduleList(request):

    print(timezone.now())

    status_list = SaleStatus.objects.all()
    professional_list = Employee.objects.all()
    client_list = Person.objects.all()
    service_list = []
    equipment_list = Equipment.objects.all()
    # event_list = list(ScheduleEvent.objects.filter(status=1).values())
    event_list = list(ScheduleEvent.objects.all().values())
    employee_list = Employee.objects.all()
    confirm_list = ScheduleEvent.objects.filter(Q(status=1) & Q(date__lt=timezone.localtime().date()) | Q(date=timezone.localtime().date(), end__lt=timezone.localtime().time()))

    for sale in Sale.objects.filter(status__pk=3):
        service_list.append({
            "pk":sale.id,
            "name":sale.service.name
        })

    context = {
        "status_list" : status_list,
        "professional_list" : professional_list,
        "client_list" : client_list,
        "service_list" : service_list,
        "equipment_list" : equipment_list,
        "event_list" : event_list,
        "employee_list":employee_list,
        "username":request.user,
        "confirm_list":confirm_list
    }

    return render(request, "html/list_schedule.html", context)

def CreateSchedule(request):
    if request.method == "POST":
        sale = get_or_none(Sale, request.POST.get("sale"))
        schedule = ScheduleEvent(
            title = "Agendamento",
            professional = get_or_none(Employee, request.POST.get("professional")),
            client = request.POST.get("_client"),
            phone = sale.client.cellphone if sale is not None  else request.POST.get("phone"),
            category = "default",
            date = request.POST.get("date"),
            start = request.POST.get("start"),
            end = request.POST.get("end"),
            status = 1,
            sale = sale,
            room = request.POST.get("room"),
            equipment = get_or_none(Equipment, request.POST.get("equipment")),
            obs = request.POST.get("obs"),
            is_courtesy = True if request.POST.get("service")=="-2" else False
        )
        print(request.POST.get("service"))
        schedule.save()
        try: 
            sale.status=SaleStatus.objects.get(pk=3)
            sale.save()
        except Exception as e:
            pass

    return redirect(reverse('schedule_list'))

def DeleteSchedule(request, schedule_id):
    if request.method=="POST":
        print("\n\n\n")
        print(request.POST)
        print("\n\n\n")

        schedule=ScheduleEvent.objects.get(pk=schedule_id)
        try:
            schedule.sale.status=SaleStatus.objects.get(pk=2)
            schedule.sale.save()
        except Exception as e:
            print(e)
            pass

        schedule.delete()

    return redirect(reverse('schedule_list'))

def PayInvoiceGroup(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]')  # Recebe o array de IDs
        payment_date=request.POST.get("payment_date")
        if payment_date !="":
            dia, mes, ano = payment_date.split('/')
            if len(ano) == 2:
                ano = '20' + ano  # ano é no século 21
            payment_date = f'{ano}-{mes.zfill(2)}-{dia.zfill(2)}'
        else:
            payment_date=datetime.date.today()
        
        for idx in ids:
            try:
                i = Invoice.objects.get(pk=idx)
                i.paid = True
                i.payment_date = payment_date

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

def ServiceAjax(request, person_id):
    service_list = []
    sale_list = Sale.objects.filter(Q(client__pk=person_id) & Q(status__id=2) & Q(service__isnull=False))
    for sale in sale_list:
        print(f"ID da Venda: {sale.id}")
        print(f"Serviço: {sale.service.name}")
        print(f"ID do Serviço: {sale.service.id}")
        service_list.append({
            "sale_id":sale.id,
            "service":sale.service.name,
            "service_id":sale.service.id
        })

    return JsonResponse(service_list, safe=False)


def ConfirmScheduleAjax(request):
    if request.method == "POST":
        ids = request.POST.getlist("ids[]")
        confirmed_list = []
        print(ids)
        for i in ids:
            s = ScheduleEvent.objects.get(pk=i)
            s.status = 2
            confirmed_list.append(s.id)
            if s.sale is not None:
                s.sale.counter+=1
                if s.sale.counter == s.sale.sessions:
                    s.sale.status = SaleStatus.objects.get(pk=5) #pk==5 é o status Concluído
                else:
                    s.sale.status = SaleStatus.objects.get(pk=2)
                s.sale.save()
            s.save()

        return JsonResponse(confirmed_list, safe=False)


@login_required(login_url="/login/")
@user_passes_test(user_is_staff, login_url="login")
def ListReceivable(request):
    invoice_list = Invoice.objects.filter(invoice_type__is_expense=False)

    context = {
        "perms":request.user.get_all_permissions(),
        "username" : request.user,
        "invoice_list" : invoice_list
    }

    return render(request, "html/list_receivable.html", context)


@login_required(login_url="/login/")
@user_passes_test(user_is_staff, login_url="login")
def CancelSale(request, sale_id):
    if request.method=="POST":
        sale = Sale.objects.get(pk=sale_id)
        sale.status=SaleStatus.objects.get(pk=4)
        sale.save()
        return JsonResponse({"success": "FUNCIONOU"})

    return redirect(reverse("list_sale"))

def saleServiceAjax(request, type_id):
    services = list(SaleService.objects.filter(service_type__id=type_id).values())

    return JsonResponse(services, safe=False)
    
def ReceiveInvoiceGroup(request):
    if request.method == "POST":
        ids = request.POST.getlist('ids[]')
        value = Decimal(request.POST.get("value"))
        payment_date=request.POST.get("payment_date")
        if payment_date !="":
            dia, mes, ano = payment_date.split('/')
            if len(ano) == 2:
                ano = '20' + ano  # ano é no século 21
            payment_date = f'{ano}-{mes.zfill(2)}-{dia.zfill(2)}'
        else:
            payment_date=datetime.date.today()

        for idx in ids:
            try:
                i = Invoice.objects.get(pk=idx)
                i.paid = True
                i.payment_date = payment_date

                i.save()
            except Invoice.DoesNotExist:
                pass  # Lidar com o caso de ID inválido

            if value < i.cost:
                inv = Invoice(
                    invoice_type = Account.objects.get(pk=112),
                    supplier = None,
                    payment_type = None,
                    generator_sale = i.generator_sale,
                    description = "Abatimento de Receita Adiantada",
                    release_date = datetime.datetime.today(),
                    due_date = payment_date,
                    payment_date = payment_date,
                    cost = i.cost-value,
                    paid = True,
                    recurring = False,
                    recurring_qtd = 0,
                    recurring_time = 0,
                    obs = "Abatimento de Receita Adiantada"
                )

                inv.save()

        response_data = {
            'success': True,
            'message': 'Contas marcadas como pagas com sucesso.'
        }
        return JsonResponse(response_data)

    response_data = {
        'error': 'Método não permitido'
    }
    return JsonResponse(response_data, status=405)