from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import FormUrl
from .models import Url

def home(request):
    form = FormUrl()
    return render(request, 'home.html', {"form": form})

def valida_url(request):
    if request.method != "POST":
        return redirect("home")  # Evita acessos indevidos via GET

    form = FormUrl(request.POST)
    host = request.META.get('HTTP_HOST')

    if not form.is_valid():
        return render(request, '404.html', {'erro': 'Dados inválidos no formulário'})

    url_personalizado = form.cleaned_data.get("url_personalizado", "").strip()

    # Verificar se a URL já existe no banco
    if url_personalizado:
        url_existente = Url.objects.filter(url_personalizado=url_personalizado).first()
        if url_existente:
            return render(request, 'existente.html', {
                'url_existente': url_existente.url_redirecionado,
                'abrir_url': f"{host}/{url_personalizado}",
            })

    try:
        url_obj = form.save(commit=False)

        # Gerar QR Code
        gerar_qrcode = request.POST.get("gerar_qrcode")
        if gerar_qrcode:
            url_obj.gerar_qr_code()

        url_obj.save()

        new_url = f"{host}/{url_obj.url_personalizado}"
        abrir_url = f"/{url_obj.url_personalizado}"
        

        context = {
            'new_url': new_url,
            'abrir_url': abrir_url,
            'qr_code': url_obj.qr_code.url if gerar_qrcode else None,
        }
        return render(request, 'sucesso.html', context)

    except Exception as e:
        return render(request, '404.html', {'erro': f"Erro ao processar a URL: {str(e)}"})

def redirecionar(request, url):
    url_obj = Url.objects.filter(url_personalizado=url).first()

    if not url_obj:
        return render(request, '404.html')

    # Verificar se a URL expirou
    if url_obj.data_expiracao and url_obj.data_expiracao < timezone.now():
        return render(request, 'expirado.html')

    # Se a URL tiver senha, pedir autenticação
    if url_obj.senha:
        if request.method == "POST":
            senha_digitada = request.POST.get("senha")
            if senha_digitada == url_obj.senha:
                return redirect(url_obj.url_redirecionado)
            return render(request, 'senha_incorreta.html', {"url": url})

        return render(request, 'pedir_senha.html', {"url": url})

    return redirect(url_obj.url_redirecionado)
