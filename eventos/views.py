from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Evento
import csv
from secrets import token_urlsafe
import os


@login_required(login_url='/usuarios/login/')
def novo_evento(request):
    if request.method == "GET":
        return render(request, 'novo_evento.html')
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        data_inicio = request.POST.get('data_inicio')
        data_termino = request.POST.get('data_termino')
        carga_horaria = request.POST.get('carga_horaria')

        cor_principal = request.POST.get('cor_principal')
        cor_secundaria = request.POST.get('cor_secundaria')
        cor_fundo = request.POST.get('cor_fundo')
        
        logo = request.FILES.get('logo')
        
        evento = Evento(
            criador=request.user,
            nome=nome,
            descricao=descricao,
            data_inicio=data_inicio,
            data_termino=data_termino,
            carga_horaria=carga_horaria,
            cor_principal=cor_principal,
            cor_secundaria=cor_secundaria,
            cor_fundo=cor_fundo,
            logo=logo,
        )
    
        evento.save()
        
        messages.add_message(request, messages.SUCCESS, 'Evento cadastrado com sucesso')
        return redirect(reverse('novo_evento'))


@login_required(login_url='/usuarios/login/')
def gerenciar_evento(request):
    nome = request.GET.get('nome')
    eventos = Evento.objects.filter(criador=request.user)

    if nome:
        eventos = eventos.filter(nome__contais=nome)

    return render(request, 'gerenciar_evento.html', {'eventos': eventos})


@login_required(login_url='/usuarios/login/')
def inscrever_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if request.method == 'GET':
        return render(request, 'inscrever_evento.html', {'evento': evento})

    elif request.method == 'POST':
        if request.user in evento.participantes.all():
            messages.add_message(request, messages.ERROR, 'Você já está inscrito nesse evento.')
            return redirect(reverse('inscrever_evento', kwargs={'id': evento_id}))
        
        evento.participantes.add(request.user)
        evento.save()

        messages.add_message(request, messages.SUCCESS, 'Inscrição realizada com sucesso.')
        return redirect(reverse('inscrever_evento', kwargs={'id': evento_id}))


@login_required(login_url='/usuarios/login/')
def participantes_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if not evento.criador == request.user:
        raise Http404('Esse evento não é seu')

    if request.method == 'GET':
        participantes = evento.participantes.all()[::3] # slice de lista do python
        return render(request, 'participantes_evento.html', {'evento': evento,
                                                             'participantes': participantes})


@login_required(login_url='/usuarios/login/')
def gerar_csv(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if not evento.criador == request.user:
        raise Http404('Esse evento não é seu')
    
    participantes = evento.participantes.all()
    
    token = f'{token_urlsafe(6)}.csv'
    path = os.path.join(settings.MEDIA_ROOT, token)

    # abre o arquivo se existe, e escreve nele, se não existe cria 
    with open(path, 'w') as arq:
        writer = csv.writer(arq, delimiter=",")
        for participante in participantes:
            x = (participante.username, participante.email)
            writer.writerow(x)

    return redirect(f'/media/{token}')