from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login, logout
# from django.contrib.auth.models import User 
# # -> User class는 내부에 정의되어 있으므로 get_user_model method로 호출한다!
from .forms import CustomUserChangeForm
from django.views.decorators.http import require_POST


def index(request):
    User = get_user_model()
    users = User.objects.all()
    content = {
        'users':users
    }
    return render(request,'accounts/index.html', content)

def signup(request):
    if request.user.is_authenticated:
        return redirect('community:index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('community:index')
    else:
        form = UserCreationForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/signup.html', context)

def detail(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, id=pk)
    context = {
        'user': user
    }
    return render(request, 'accounts/detail.html', context)

def signin(request):
    if request.user.is_authenticated:
        return redirect('community:index')
    if request.method == 'POST':
        # 사용자가 보낸 값 -> form
        form = AuthenticationForm(request, request.POST)
        # 검증
        if form.is_valid():
            # 검증 완료 시 로그인
            login(request, form.get_user())
            
            # [단축평가]
            # or 일 때, 앞에가 False면 뒤에도 검사!
            return redirect(request.GET.get('next') or 'community:index')
    else:    
        form = AuthenticationForm()
    context = {
        'form':form 
    }
    return render(request, 'accounts/signin.html', context)


@login_required
# annotation으로 하지 않고, 조건식으로 직접 작성해도 된다~!
def signout(request):
    logout(request)
    return redirect('community:index')

@require_POST
@login_required
def delete(request):
    request.user.delete()
    return redirect('community:index')

def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('community:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context ={
        'form':form
    }
    return render(request, 'accounts/update.html', context)