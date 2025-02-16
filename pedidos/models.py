from django.db import models

# Create your models here.
from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()

    def __str__(self):
        return self.nome

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Pizza(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    ingredientes = models.TextField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='pizzas/', null=True, blank=True)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    pizzas = models.ManyToManyField(Pizza)
    status = models.CharField(max_length=20, choices=[('Pendente', 'Pendente'), ('Em Preparo', 'Em Preparo'), ('Entregue', 'Entregue')], default='Pendente')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.status}"
