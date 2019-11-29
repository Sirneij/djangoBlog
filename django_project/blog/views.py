from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from hitcount.views import HitCountDetailView
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.contrib.auth.models import User
from .models import Post, Comment
from .forms import PostForm, UpdatePostForm, CommentForm
from django.template.loader import render_to_string




def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    common_tags = Post.tags.most_common()[:4]
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 5) # 5 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', {'page': page, 'posts': posts, 'tag': tag, 'common_tags': common_tags})

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'
    paginate_by = 5


# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    post_tags_ids = post.tags.values_list('id', flat=True)
    is_ovated = False
    if post.ovation.filter(id=request.user.id).exists():
        is_ovated = True
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[:4]
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            body = request.POST.get('body')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post, author=request.user, body=body, reply=comment_qs)
            comment.save()
            #return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
    context = {
    'post': post, 
    'similar_posts': similar_posts,
    'comments': comments,
    'comment_form': comment_form,
    'is_ovated': is_ovated,
    'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:1],
    #'total_ovations': total_ovations,
    }

    if request.is_ajax():
        html = render_to_string('blog/comments.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'blog/post_detail.html', context)

def post_new(request):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.title)
        # newpost.author = request.user
        newpost.save()
        form.save_m2m()
        return HttpResponseRedirect(newpost.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "blog/post_form.html", context)

class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class=PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    # success_url = 'blog/index.html'

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class=UpdatePostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_staff:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_staff:
            return True
        return False


class SearchResultsView(generic.ListView):
    model = Post
    template_name = 'blog/search_results.html'
    
    def get_queryset(self): 
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
                Q(title__icontains=query)|
                Q(body__icontains=query)|
                Q(author__username__icontains=query)
                ).distinct()
        return object_list

@login_required
def ovation(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_ovated = False
    if post.ovation.filter(id=request.user.id).exists():
        post.ovation.remove(request.user)
        is_ovated = False
    else:
        post.ovation.add(request.user)
        is_ovated = True
    return HttpResponseRedirect(post.get_absolute_url()) 