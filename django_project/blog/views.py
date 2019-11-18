from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from taggit.models import Tag
from django.db.models import Count, Q
from comments.forms import CommentForm
from comments.models import Comment
from django.contrib.auth.models import User
from .models import Post#, Comment
from .forms import PostForm, UpdatePostForm#, CommentForm




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
    
    # List of active comments for this post
    # comments = post.comments.filter(active=True)

    # new_comment = None

    # if request.method == 'POST':
    #     # A comment was posted
    #     comment_form = CommentForm(data=request.POST)
    #     if comment_form.is_valid():
    #         # Create Comment object but don't save to database yet
    #         new_comment = comment_form.save(commit=False)
    #         # Assign the current post to the comment
    #         new_comment.post = post
    #         # Save the comment to the database
    #         new_comment.save()
    # else:
    #     comment_form = CommentForm()
    
    # List of similar posts
    initial_data = {
            "content_type": post.get_content_type,
            "object_id": post.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()


        new_comment, created = Comment.objects.get_or_create(
                            user = request.user,
                            content_type= content_type,
                            object_id = obj_id,
                            content = content_data,
                            parent = parent_obj,
                        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())


    comments = post.comments
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[:4]

    context = {
    'post': post, 
    # 'new_comment': new_comment, 
    # 'comment_form': comment_form, 
    "comments": comments,
    "comment_form":form, 
    'similar_posts': similar_posts
    }

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
                Q(author__first_name__icontains=query)|
                Q(author__last_name__icontains=query)|
                Q(author__username__icontains=query)
                ).distinct()
        return object_list