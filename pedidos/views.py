from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Pedido, Pizza, Cliente, Category
from decimal import Decimal

def listar_pedidos(request):
    """View function to list all orders"""
    pedidos = Pedido.objects.all()
    return render(request, 'pedidos/listar_pedidos.html', {'pedidos': pedidos})

def criar_pedido(request):
    """View function to create a new order"""
    return render(request, 'pedidos/criar_pedido.html')

def menu(request):
    pizzas = Pizza.objects.all()
    categories = Category.objects.all()

    search_query = request.GET.get('search')
    category_id = request.GET.get('category')

    if search_query:
        pizzas = pizzas.filter(nome__icontains=search_query)
        if not pizzas:
            messages.warning(request, f'Nenhuma pizza encontrada com o termo "{search_query}".')

    if category_id:
        pizzas = pizzas.filter(category_id=category_id)

    return render(request, 'pedidos/menu.html', {
        'pizzas': pizzas,
        'categories': categories,
        'search': search_query,
    })

def carrinho(request):
    if 'carrinho' not in request.session:
        request.session['carrinho'] = []
    
    carrinho_items = []
    total = 0
    
    try:
        for item in request.session['carrinho']:
            if isinstance(item, dict):  # Verify if item is a dictionary
                pizza = get_object_or_404(Pizza, id=item['pizza_id'])
                carrinho_items.append({
                    'nome': pizza.nome,
                    'tamanho': item['tamanho'],
                    'borda': item['borda'],
                    'preco': item['preco'],
                    'observacoes': item.get('observacoes', ''),
                    'id': item['pizza_id'],
                    'category': pizza.category.name if pizza.category else None,
                })
                total += float(item['preco'])
    except (TypeError, KeyError):
        # If there's an error, reset the cart
        request.session['carrinho'] = []
        messages.error(request, 'Erro no carrinho. O carrinho foi limpo.')
    
    return render(request, 'pedidos/carrinho.html', {
        'carrinho_items': carrinho_items,
        'total': total
    })

def adicionar_carrinho(request, pizza_id):
    if request.method == 'POST':
        pizza = get_object_or_404(Pizza, id=pizza_id)
        tamanho = request.POST.get('tamanho')
        borda = request.POST.get('borda')
        observacoes = request.POST.get('observacoes', '')
        
        # Calculate base price
        preco_base = float(pizza.preco)
        
        # Add size price
        if tamanho == 'M':
            preco_base += 10.00
        elif tamanho == 'G':
            preco_base += 20.00
            
        # Create cart item
        item = {
            'pizza_id': pizza_id,
            'tamanho': tamanho,
            'borda': borda,
            'preco': preco_base,
            'observacoes': observacoes
        }
        
        if 'carrinho' not in request.session:
            request.session['carrinho'] = []
            
        request.session['carrinho'].append(item)
        request.session.modified = True
        
        messages.success(request, f'{pizza.nome} adicionada ao carrinho!')
        return redirect('pedidos:carrinho')
    
    return redirect('pedidos:pizza_detalhes', pizza_id=pizza_id)

def remover_carrinho(request, index):
    if request.method == 'POST':
        if 'carrinho' in request.session:
            carrinho = request.session['carrinho']
            if 0 <= index < len(carrinho):
                del carrinho[index]
                request.session.modified = True
                messages.success(request, 'Item removido do carrinho!')
    
    return redirect('pedidos:carrinho')

def pizza_detalhes(request, pizza_id):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    return render(request, 'pedidos/pizza_detalhes.html', {'pizza': pizza, 'category': pizza.category})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('pedidos:menu')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserCreationForm()

    return render(request, 'pedidos/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Você está logado como {username}!")
                return redirect("pedidos:menu")
            else:
                messages.error(request,"Usuário ou senha inválidos.")
        else:
            messages.error(request,"Usuário ou senha inválidos.")
    form = AuthenticationForm()
    return render(request, "pedidos/login.html", {"form":form})

@login_required(login_url='pedidos:login')
def checkout(request):
    if request.method == 'POST':
        if not request.session.get('carrinho'):
            messages.error(request, 'Seu carrinho está vazio')
            return redirect('pedidos:carrinho')
        
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        
        # Create or get customer
        cliente, created = Cliente.objects.get_or_create(
            telefone=telefone,
            defaults={'nome': nome, 'endereco': endereco}
        )
        
        # Create order
        pedido = Pedido.objects.create(
            cliente=cliente,
            status='Pendente'
        )
        
        # Add pizzas to order
        for item in request.session['carrinho']:
            pizza = Pizza.objects.get(id=item['pizza_id'])
            pedido.pizzas.add(pizza)
        
        # Clear cart
        request.session['carrinho'] = []
        request.session.modified = True
        
        messages.success(request, 'Pedido realizado com sucesso!')
        return redirect('pedidos:menu')
        
    return render(request, 'pedidos/checkout.html')
