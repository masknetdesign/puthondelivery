from django.contrib import admin
from .models import Cliente, Pizza, Pedido, Category

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "telefone", "endereco")
    search_fields = ("nome", "telefone")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "preco", "image", "category")
    search_fields = ("nome",)
    fields = ("category", "nome", "ingredientes", "preco", "image")

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "status", "criado_em")
    list_filter = ("status", "criado_em")
    search_fields = ("cliente__nome",)
