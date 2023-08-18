from django.db import models
import datetime
# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=50)
    cpf = models.CharField(max_length=14)
    birth_date = models.DateField()
    gender = models.ForeignKey("Gender", null=True, blank=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=14)
    cellphone = models.CharField(max_length=15)
    email = models.EmailField(max_length=128)
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

class Employee(models.Model): #Employee = User?
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
    description = models.CharField(max_length=200)
    release_date = models.DateField()
    payment_date = models.DateField(blank=True, null=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)
    recurring = models.BooleanField(default=False)
    recurring_qtd = models.IntegerField(blank=True, null=True)
    recurring_time = models.IntegerField(blank=True, null=True)
    obs = models.CharField(max_length=200)

class Sale(models.Model):
    sale_type = models.ForeignKey("SaleType", null=True, blank=True, on_delete=models.SET_NULL) #plano, produto ou serviço
    account = models.ForeignKey("Account", null=True, blank=True, on_delete=models.SET_NULL)
    client = models.ForeignKey("Person", null=True, blank=True, on_delete=models.CASCADE)
    seller = models.ForeignKey("Employee", null=True, blank=True, on_delete=models.SET_NULL)
    status = models.ForeignKey("SaleStatus", null=True, blank=True, on_delete=models.SET_NULL)
    origin = models.ForeignKey("SaleOrigin", null=True, blank=True, on_delete=models.SET_NULL)
    service = models.ForeignKey("SaleService", null=True, blank=True, on_delete=models.SET_NULL) #service = o que estão vendendo
    payment_type = models.ForeignKey("PaymentType", null=True, blank=True, on_delete=models.SET_NULL)
    discount_is_percent = models.BooleanField(default=False)
    discount = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=8)
    sessions = models.IntegerField(null=True, blank=True)
    obs = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    final_price = models.DecimalField(max_digits=8, null=True, blank=True, decimal_places=2)

class SaleType(models.Model): #plano, produto ou serviço 
    name = models.CharField(max_length=80, verbose_name="Nome")

    def __str__(self):
        return self.name

class SaleService(models.Model):
    service_type = models.ForeignKey("SaleType", null=True, blank=True, on_delete=models.CASCADE, verbose_name="Tipo")
    name = models.CharField(max_length=100, verbose_name="Nome")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Preço")
    sessions = models.IntegerField(null=True, blank=True, verbose_name="Qtd. de Sessões")

    class Meta:
        verbose_name="Tipo de Venda"
        verbose_name_plural="Tipos de Venda"

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

class Service(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=40, verbose_name="Nome Fantasia", default="")
    cnpj = models.CharField(max_length=40, verbose_name="CNPJ", default="")
    address = models.CharField(max_length=40, verbose_name="Endereço", default="")
    cep = models.CharField(max_length=40, verbose_name="CEP", default="")

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
    title = models.CharField(max_length=20)
    professional = models.ForeignKey("Employee", on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey("Person", on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=10, default="time")
    date = models.DateField(null=True, blank=True)
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)
    status = models.ForeignKey("SaleStatus", on_delete=models.SET_NULL, blank=True, null=True) #SaleStatus pois os status são os mesmos.
    service = models.ForeignKey("SaleService", on_delete=models.SET_NULL, blank=True, null=True)
    sessions = models.IntegerField(null=True, blank=True,)
    room = models.CharField(max_length=20, null=True, blank=True)
    equipment = models.ForeignKey("Equipment", on_delete=models.CASCADE, null=True, blank=True)
    obs = models.CharField(max_length=50, null=True, blank=True)

class ScheduleStatus(models.Model):
    name = models.CharField(max_length=15)

class Equipment(models.Model):
    name = models.CharField(max_length=40)