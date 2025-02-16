from django.shortcuts import render, redirect
from django.http import HttpResponse

def listar_pedidos(request):
    """View function to list all orders"""
    return HttpResponse("Lista de pedidos")

def criar_pedido(request):
    """View function to create a new order"""
    return HttpResponse("Criar novo pedido")