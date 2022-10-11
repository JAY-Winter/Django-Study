from traceback import format_exc
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

# 게시글 별 내용 확인
def detail(request, pk):
    forum = Forum.objects.get(pk=pk)
    context = {
        'forum' : forum,
    }
    return render(request, 'forums/detail.html', context)

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
    
# 게시글 수정
def update(request, pk):
    forum = Forum.objects.get(pk=pk)
    if request.method == 'POST':
        form = ForumForm(request.POST, instance=forum)
        if form.is_valid():
            form.save()
            return redirect('forums:detail', forum.pk)
    else:
        form = ForumForm(instance=forum)
    context = {
        'form' : form,
        'forum': forum,
    }
    return render(request, 'forums/update.html', context)

def delete():
    pass