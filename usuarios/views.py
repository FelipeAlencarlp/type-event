from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages, auth

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not (senha == confirmar_senha):
            messages.add_message(request, messages.ERROR, 'As senhas não são iguais.')
            return redirect(reverse('cadastro'))
        
        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, messages.ERROR, 'O nome de usuário já existe')
            return redirect(reverse('cadastro'))
        
        try:
            user = User.objects.create_user(username=username, email=email, password=senha)
            user.save()

            messages.add_message(request, messages.SUCCESS, 'Cadastro realizado com sucesso! Entre com suas credenciais.')
            return redirect(reverse('login'))
        
        except:
            messages.add_message(request, messages.ERROR, 'Erro interno do sistema! Contate um administrador.')
            return redirect(reverse('cadastro'))


def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=username, password=senha)

        if not user:
            messages.add_message(request, messages.ERROR, 'Nome de usuário ou senha inválidos')
            return redirect(reverse('login'))
        
        auth.login(request, user)
        return redirect('/eventos/novo_evento/')