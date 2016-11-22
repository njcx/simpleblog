from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.contrib.auth import logout


# def post_list(request):
#     #postsAll = Post.objects.annotate(num_comment=Count('comment')).filter(published_date__isnull=False).prefetch_related('category').prefetch_related('tags').order_by('-published_date')
#     postsAll = Post.objects.annotate(num_comment=Count('id')).filter(published_date__isnull=False).order_by('-published_date')
#     #for p in postsAll:
#     #    p.click = cache_manager.get_click(p)
#     # Show 10 contacts per page
#     paginator = Paginator(postsAll, 10)  
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver last page of results.
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post_list.html', {'posts': posts, 'page': True})

def post_list(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts}) 

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

@login_required
def post_new(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)




def logout_view(request):
    logout(request)