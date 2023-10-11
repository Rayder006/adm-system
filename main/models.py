from django.core.validators import MaxValueValidator
from django.utils import timezone
from django.db.models import Q
from django.db import models
import datetime
# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=50)
    cpf = models.CharField(max_length=14)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.ForeignKey("Gender", null=True, blank=True, on_delete=models.SET_NULL)
    # phone = models.CharField(max_length=14)
    cellphone = models.CharField(max_length=15)
    email = models.EmailField(max_length=128, null=True, blank=True)
    cep = models.CharField(max_length=9, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    district = models.CharField(max_length=30, null=True, blank=True)
    UF = models.CharField(max_length=2, null=True, blank=True)
    complement = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class Gender(models.Model): 
    name= models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nome")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

class Invoice(models.Model):
    invoice_type = models.ForeignKey("Account", null=True, blank=True, on_delete=models.SET_NULL)
    supplier = models.ForeignKey("Supplier", null=True, blank=True, on_delete=models.SET_NULL)
    payment_type = models.ForeignKey("PaymentType", null=True, blank=True, on_delete=models.SET_NULL)
    generator_sale = models.ForeignKey("Sale", null=True, blank=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    release_date = models.DateField()
    due_date = models.DateField()
    payment_date = models.DateField(blank=True, null=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)
    recurring = models.BooleanField(default=False)
    recurring_qtd = models.IntegerField(blank=True, null=True)
    recurring_time = models.IntegerField(blank=True, null=True)
    obs = models.CharField(max_length=200)

    def __str__(self):
        return self.release_date.strftime('%d/%m/%Y') + " - " + self.supplier.name if self.supplier else self.release_date.strftime('%d/%m/%Y') + " - Automático"

class Sale(models.Model):
    client = models.ForeignKey("Person", null=True, blank=True, on_delete=models.CASCADE)
    seller = models.ForeignKey("Employee", null=True, blank=True, on_delete=models.SET_NULL)
    status = models.ForeignKey("SaleStatus", null=True, blank=True, on_delete=models.SET_NULL)
    origin = models.ForeignKey("SaleOrigin", null=True, blank=True, on_delete=models.SET_NULL)
    service = models.ForeignKey("SaleService", null=True, blank=True, on_delete=models.SET_NULL) #service = o que estão vendendo
    payment_type = models.ForeignKey("PaymentType", null=True, blank=True, on_delete=models.SET_NULL, related_name="payment1")
    payment_type2 = models.ForeignKey("PaymentType", null=True, blank=True, on_delete=models.SET_NULL, related_name="payment2")
    discount = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8)
    sessions = models.IntegerField(null=True, blank=True)
    obs = models.CharField(max_length=200, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    contract_date = models.DateTimeField(null=True, blank=True)
    counter = models.IntegerField(default=0)
    price1 = models.DecimalField(max_digits=8, null=True, blank=True, decimal_places=2)
    price2 = models.DecimalField(max_digits=8, null=True, blank=True, decimal_places=2)
    installments1 = models.IntegerField(default=1)
    installments2 = models.IntegerField(blank=True, null=True)
    final_price = models.DecimalField(max_digits=8, null=True, blank=True, decimal_places=2)

    def __str__(self):
        return f"{self.client.name} - {self.release_date}"

class SaleType(models.Model): #plano, produto ou serviço 
    name = models.CharField(max_length=80, verbose_name="Nome")

    def __str__(self):
        return self.name

class SaleService(models.Model):
    service_type = models.ForeignKey("SaleType", null=True, blank=True, on_delete=models.CASCADE, verbose_name="Tipo")
    name = models.CharField(max_length=100, verbose_name="Nome")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Preço")
    sessions = models.IntegerField(null=True, blank=True, verbose_name="Qtd. de Sessões")
    account = models.ForeignKey("Account", null=True, blank=True, verbose_name="Conta", on_delete=models.SET_NULL)
    services_offered = models.ManyToManyField('self', through='ServiceRelationship', symmetrical=False, verbose_name="Serviços Oferecidos (Caso Plano)")
    plan_service_relation = models.ManyToManyField('self', blank=True, null=True, limit_choices_to=~Q(service_type__pk__in=[1, 4]))


    class Meta:
        verbose_name="Serviço"
        verbose_name_plural="Serviços Oferecidos"

    def __str__(self):
        return self.name

class SaleStatus(models.Model): #novo, pendente, agendado ou cancelado
    name = models.CharField(max_length=20, verbose_name="Nome")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Status de Venda"
        verbose_name_plural="Status de Venda"

class Account(models.Model):
    number = models.CharField(max_length=30, verbose_name="Código")
    name = models.CharField(max_length=80, verbose_name="Descrição Sistema")
    is_expense = models.BooleanField(verbose_name="Saída?")
    account_type = models.ForeignKey("AccountType", on_delete=models.CASCADE, verbose_name="Tipo")
    commentary = models.CharField(max_length=50, verbose_name="Comentário")

    def __str__(self):
        return self.number
    
    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'

class AccountType(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nome")
    
    class Meta:
        verbose_name="Tipo de Conta"
        verbose_name_plural="Tipos de Conta"

    def __str__(self):
        return self.name

class PaymentType(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nome")
    has_tax = models.BooleanField(default=False, verbose_name="Tem Taxa?")
    taxa = models.DecimalField(max_digits=5, decimal_places=2, verbose_name = 'Dias p/ recebimento', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Forma de Pagamento"
        verbose_name_plural="Formas de Pagamento"

class Tax(models.Model):
    name = models.CharField(max_length=30, verbose_name = 'Nome')
    tax = models.DecimalField(max_digits=5, decimal_places=2, verbose_name = 'Taxa (%)')
    payment_type = models.ForeignKey("PaymentType", on_delete=models.CASCADE, verbose_name = 'Forma de Pagamento Vinculada')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Taxa'
        verbose_name_plural = 'Taxas'

class Supplier(models.Model):
    name = models.CharField(max_length=40, verbose_name="Nome Fantasia", default="")
    cnpj = models.CharField(max_length=40, verbose_name="CNPJ", default="")
    address = models.CharField(max_length=40, verbose_name="Endereço", default="", null=True, blank=True)
    cep = models.CharField(max_length=40, verbose_name="CEP", default="", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'

class SaleOrigin(models.Model):
    name = models.CharField(max_length=40, verbose_name="Nome")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Origem de Venda'
        verbose_name_plural = 'Origens de Venda'

class ScheduleEvent(models.Model): 
    title = models.CharField(max_length=250)
    professional = models.ForeignKey("Employee", on_delete=models.CASCADE, null=True, blank=True)
    client = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, default="time")
    date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)
    sale = models.ForeignKey("Sale", on_delete=models.SET_NULL, blank=True, null=True)
    status = models.IntegerField()
    room = models.CharField(max_length=80, null=True, blank=True)
    equipment = models.ForeignKey("Equipment", on_delete=models.CASCADE, null=True, blank=True)
    obs = models.CharField(max_length=350, null=True, blank=True)
    is_courtesy = models.BooleanField(default=False)

class ScheduleStatus(models.Model):
    name = models.CharField(max_length=15)

class Equipment(models.Model):
    name = models.CharField(max_length=40)

class Meta(models.Model):
    mes = models.PositiveIntegerField(null=True, validators=[MaxValueValidator(12)])
    ano = models.PositiveIntegerField(null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.mes}/{self.ano} - R$" + '{:.2f}'.format(self.valor)

class ServiceRelationship(models.Model):
    from_service = models.ForeignKey(SaleService, on_delete=models.CASCADE, unique=True, related_name='Plano', verbose_name="Plano", limit_choices_to=Q(service_type__pk=1))
    to_services = models.ManyToManyField(SaleService, related_name='Serviços', verbose_name="Serviços Oferecidos", limit_choices_to=~Q(service_type__pk__in=[1, 4]))

    class Meta:
        verbose_name="Relação Plano-Serviços"
        verbose_name_plural="Relações Plano-Serviços"
