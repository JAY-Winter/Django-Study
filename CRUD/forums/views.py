from django.shortcuts import redirect, render
from .forms import ForumForm
from .models import Forum

# Create your views here.
def index(request):
    forums = Forum.objects.all()
    context = {
        'forums' : forums,
    }
    return render(request, 'forums/index.html', context)

def detail():
    pass

# 게시글 작성
def create(request):
    # 게시글 작성 버튼을 눌렀을 때
    if request.method == 'POST':
        form = ForumForm(request.POST)
        # 작성할 게시글이 유효한지 확인
        if form.is_valid():
            form.save()
            return redirect('forums:index')
    # 게시글 작성 페이지 렌더링을 요청할 때 
    else:
        form = ForumForm()
    context = {
        'form' : form,
    }
    return render(request, 'forums/create.html', context)

def update():
    pass

def delete():
    pass