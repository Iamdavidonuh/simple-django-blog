from django.shortcuts import render,get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,CreateView,DeleteView,UpdateView
from django.views.generic.edit import FormMixin
from .models import Post,Comment
from users.forms import CommentForm
# Create your views here.

def home(request):
    context = {'posts':Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'#<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'#<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView, FormMixin):
    model = Post
    fields = ['name','email','body']
    form_class = CommentForm
    context_object_name = 'posts'
    '''
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk':self.object.id})
'''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #queryset for all comments
        context['form'] = CommentForm(initial = {'post':self.object} )
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        comment=form.save(commit=False)
        post_id = get_object_or_404(Post,id=self.kwargs.get('id'))
        comment.post = post_id
        comment.save()
        return super().form_valid(form)



class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
def about(request):
    return render(request, 'blog/about.html', {'title':'About'})