from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import authenticate, login, logout, get_backends
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from dateutil.relativedelta import relativedelta
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.core import serializers
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from .forms import MetaForm
from decimal import Decimal
from .functions import *
from .models import *
import locale
import calendar

def LeftWorkDays():
    hoje = datetime.datetime.now()
    ano_atual = hoje.year
    mes_atual = hoje.month
    dia_atual = hoje.day

    dias_uteis_totais = WorkDays(ano_atual, mes_atual)
    dias_uteis_passados = 0

    for dia in range(1, dia_atual + 1):
        if calendar.weekday(ano_atual, mes_atual, dia) < 5:
            dias_uteis_passados += 1

    dias_uteis_restantes = dias_uteis_totais - dias_uteis_passados
    return dias_uteis_restantes+1

def WorkDays(ano, mes):
    num_dias = calendar.monthrange(ano, mes)[1]
    
    dias_uteis = 0
    
    for dia in range(1, num_dias + 1):
        if calendar.weekday(ano, mes, dia) < 5:  # 0 a 4 representa dias úteis (de segunda a sexta)
            dias_uteis += 1
            
    return dias_uteis

def createRecurringInvoice(inv_pk):
    inv = Invoice.objects.get(pk=inv_pk)
    recurring_time = Invoice.objects.get(pk=inv_pk).recurring_time
    
    for i in range(0, inv.recurring_qtd):
        inv_ = inv
        inv_.pk = None
        inv_.recurring_qtd -= 1
        print(inv_.release_date)
        inv_.release_date = inv_.release_date + datetime.timedelta(days=inv_.recurring_time) if inv_.recurring_time!=30 else inv_.release_date + relativedelta(months=1)
        inv_.due_date = inv_.due_date + datetime.timedelta(days=inv_.recurring_time) if inv_.recurring_time!=30 else inv_.due_date + relativedelta(months=1)

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
    service_list=[]
    if sale.status.pk == 1:
        sale.status = SaleStatus.objects.get(pk=2)
        sale.contract_date = datetime.datetime.today()
        sale.save()
    
    if sale.contract_date is None:
        sale.contract_date = datetime.datetime.today()
        sale.save()

    if sale.service.service_type.pk==1: #plano
        try:
            services = ServiceRelationship.objects.get(from_service__pk=sale.pk)
            for service in services.to_services:
                service_list.append(service.name)
        except Exception as e:
            service_list.append("Nenhum Serviço Cadastrado")
            pass

    due_date = (sale.release_date + datetime.timedelta(days=365)).strftime("%d/%m/%Y")
    parcela1 = Decimal(sale.price1 / sale.installments1)
    parcela2 = sale.price2 / sale.installments2 if sale.price2 else 0
    today = sale.contract_date

    qtd_parcelas1 = []

    for i in range(1, sale.installments1+1):
        qtd_parcelas1.append(i)

    context = {
        "sale":sale,
        "user":request.user,
        "due_date":due_date,
        "parcela1":'{:.2f}'.format(parcela1),
        "parcela2":'{:.2f}'.format(parcela2),
        "qtd_parcelas1":qtd_parcelas1,
        "today":today,
        "service_list":service_list
    }
    if sale.service.service_type.pk==1: #plano
        return render(request, 'contracts/plano.html', context)
    elif sale.service.service_type.pk==4: #pilates
        return render(request, 'contracts/pilates.html', context)
    else:
        return render(request, 'contracts/esteticos.html', context)

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
    locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
    today = datetime.datetime.today()
    try:
        meta = Meta.objects.get(mes=today.month, ano=today.year).valor
    except Meta.DoesNotExist:
        meta= Decimal(0.00)
    vendido=0
    vendas = Sale.objects.filter(release_date__month=today.month, release_date__year=today.year)

    for venda in vendas:
        vendido += venda.final_price

    context={
        "uteis": LeftWorkDays(),
        "vendido":locale.currency(vendido, grouping=True, symbol=False),
        "meta":locale.currency(meta, grouping=True, symbol=False),
        "falta": locale.currency(meta-vendido, grouping=True, symbol=False),
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
        invoice.supplier = get_or_none(Supplier, request.POST.get("supplier"))
        invoice.description = request.POST.get("description")
        invoice.release_date = request.POST.get("release_date")
        invoice.due_date = request.POST.get("due_date")
        invoice.cost = request.POST.get("cost")[3:].replace(".", "").replace(",", ".")
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
    for sale in sale_list:
        sale.available=sale.sessions-sale.counter
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
        discount = service.price * service.sessions
        discount -= final_price
        payment_type = get_or_none(PaymentType, request.POST.get("payment_type"))
        payment_type2 = None if request.POST.get("mixed") == 0 else get_or_none(PaymentType, request.POST.get("payment_type"))
        installments1=int(request.POST.get("installments1")) if request.POST.get("installments1") else 1
        installments2=int(request.POST.get("installments2")) if request.POST.get("installments2") else 0
        mixed = request.POST.get("mixed")==1
        price1 = Decimal(request.POST.get("price1"))
        price2 = Decimal(request.POST.get("price2")) if mixed==1 else None


        s = Sale(
            client = get_or_none(Person, request.POST.get("client")),
            seller = get_or_none(Employee, request.POST.get("seller")),
            status = SaleStatus.objects.get(pk=1), # novo
            origin = get_or_none(SaleOrigin, request.POST.get("sale_origin")),
            service = service,
            payment_type = payment_type,
            payment_type2 = payment_type2,
            discount = discount if discount>0 else discount * (-1),
            sessions = request.POST.get("sessions"),
            obs = request.POST.get("obs"),
            release_date = request.POST.get("date"),
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
        "sale" : sale,
        "available":sale.sessions-sale.counter
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
    confirm_list = ScheduleEvent.objects.filter(Q(status=1) & (Q(date__lt=timezone.localtime().date()) | Q(date=timezone.localtime().date(), end__lt=timezone.localtime().time())))

    for sale in Sale.objects.filter(status__pk=3):
        service_list.append({
            "pk":sale.id,
            "name":sale.service.name
        })

    for event in event_list:
        event['professional_name'] = Employee.objects.get(pk=event['professional_id']).name
        try:
            event['client_id'] = Person.objects.get(name=event['client']).pk
        except Exception as e:
            event['client_id'] = None

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
        category = ""
        is_courtesy = True if request.POST.get("service")=="-2" else False
        if sale is not None:
            category=sale.service.service_type.name
        else:
            category = "Cortesia" if is_courtesy else "Avaliação"

        schedule = ScheduleEvent(
            title = category,
            professional = get_or_none(Employee, request.POST.get("professional")),
            client = request.POST.get("_client"),
            phone = sale.client.cellphone if sale is not None  else request.POST.get("phone"),
            category = category,
            date = request.POST.get("date"),
            start = request.POST.get("start"),
            end = request.POST.get("end"),
            status = 1,
            sale = sale,
            room = request.POST.get("room"),
            equipment = get_or_none(Equipment, request.POST.get("equipment")),
            obs = request.POST.get("obs"),
            is_courtesy = is_courtesy
        )
        print(request.POST.get("service"))
        schedule.save()
        if sale is not None: 
            sale.status=SaleStatus.objects.get(pk=3)
            sale.counter+=1
            sale.save()

    return redirect(reverse('schedule_list'))

def EditSchedule(request, schedule_id):
    if request.method == "POST":
        schedule=ScheduleEvent.objects.get(pk=schedule_id)
        if schedule.status!=1:
            return redirect(reverse("schedule_list"))
        sale = get_or_none(Sale, request.POST.get("sale"))
        category = ""
        is_courtesy = True if request.POST.get("service")=="-2" else False
        if sale is not None:
            category=sale.service.service_type.name
            sale.counter-=1
            sale.save()
        else:
            category = "Cortesia" if is_courtesy else "Avaliação"

        schedule.title = category
        schedule.professional = get_or_none(Employee, request.POST.get("professional"))
        schedule.client = request.POST.get("_client")
        schedule.phone = sale.client.cellphone if sale is not None  else request.POST.get("phone")
        schedule.category = category
        schedule.date = request.POST.get("date")
        schedule.start = request.POST.get("start")
        schedule.end = request.POST.get("end")
        schedule.status = 1
        schedule.sale = sale
        schedule.room = request.POST.get("room")
        schedule.equipment = get_or_none(Equipment, request.POST.get("equipment"))
        schedule.obs = request.POST.get("obs")
        schedule.is_courtesy = is_courtesy
        
        print(request.POST.get("service"))
        schedule.save()
        if schedule.sale is not None: 
            sale.status=SaleStatus.objects.get(pk=3)
            sale.counter+=1
            schedule.sale.save()

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
    response = []
    service_list = []
    sale_list = Sale.objects.filter(Q(client__pk=person_id) & (Q(status__id=2) & Q(status__id=3)) & Q(service__isnull=False))
    for sale in sale_list:
        print(f"ID da Venda: {sale.id}")
        print(f"Serviço: {sale.service.name}")
        print(f"ID do Serviço: {sale.service.id}")
        if sale.counter < sale.sessions:
            service_list.append({
                "sale_id":sale.id,
                "service": sale.service.name + " - " + sale.sessions - sale.counter + " disponíveis",
                "service_id":sale.service.id
            })
    response.append(Person.objects.get(pk=person_id).cellphone)
    response.append(service_list)

    return JsonResponse(response, safe=False)


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
                if s.sale.counter == s.sale.sessions:
                    s.sale.status = SaleStatus.objects.get(pk=4) #pk==4 é o status Concluído
                s.sale.save()
            s.save()

        return JsonResponse(confirmed_list, safe=False)

def UnconfirmScheduleAjax(request):
    if request.method == "POST":
        ids = request.POST.getlist("ids[]")
        unconfirmed_list = []
        print(ids)
        for i in ids:
            s = ScheduleEvent.objects.get(pk=i)
            s.status = 3
            unconfirmed_list.append(s.id)
            if s.sale is not None:
                s.sale.counter -= 1
                s.sale.save()
            s.save()

        return JsonResponse(unconfirmed_list, safe=False)


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