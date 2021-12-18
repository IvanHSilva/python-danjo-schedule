from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def emptyfield(request, field, title):
    # messages.info(request, field)
    if not field:
        messages.error(request, f'O campo {title} deve ser preenchido!')
        return render(request, 'accounts/register.html')

def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    user = request.POST.get('user')
    password = request.POST.get('password')
    userlog = auth.authenticate(request, username=user, password=password)
    if not userlog:
        messages.error(request, 'Usuário ou senha inválidos!')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, userlog)
        messages.success(request, 'Usuário logado com sucesso!')
        return redirect('dashboard')

def logout(request):
    auth.logout(request)
    return redirect('login')
    # return render(request, 'accounts/logout.html')

def register(request):
    # if request.method != 'post':
    #     return render(request, 'accounts/register.html')

    name = request.POST.get('name')
    email = request.POST.get('email')
    user = request.POST.get('user')
    password = request.POST.get('password')
    confpass = request.POST.get('confpass')
    # messages.info(request, f'Campos: {request.method}, {name}, {email}, {user}, {password}')
    # print( f'Campos: {request.method}, {name}, {email}, {user}, {password}')

    # validate fields
    emptyfield(request, name, 'Nome')
    emptyfield(request, email, 'E-Mail')
    emptyfield(request, user, 'Usuário')
    emptyfield(request, password, 'Senha')
    emptyfield(request, confpass, 'Confirmar Senha')
    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido!')
        return render(request, 'accounts/register.html')
    if len(user) < 6:
        messages.error(request, 'Usuário deve ter ao menos 6 letras!')
        return render(request, 'accounts/register.html')
    if len(password) < 6:
        messages.error(request, 'Senha deve ter ao menos 6 letras!')
        return render(request, 'accounts/register.html')
    if confpass:
        if password != confpass:
            messages.error(request, 'Confirmação da senha diferente da senha!')
            return render(request, 'accounts/register.html')
    else:
        return render(request, 'accounts/register.html')
    if User.objects.filter(username=user).exists():
        messages.error(request, 'Usuário já cadastrado!')
        return render(request, 'accounts/register.html')
    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já cadastrado!')
        return render(request, 'accounts/register.html')

    messages.success(request, 'Usuário cadastrado com sucesso!')
    newuser = User.objects.create_user(username=user, email= email,
                                       password=password, first_name=name)
    newuser.save()
    return redirect(login)

@login_required(redirect_field_name='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
