from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy

#base group
from django.views import View

#display group: list & detail module
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin

#edit group
from django.views.generic.edit import CreateView, FormView
#from django.views.generic.edit import UpdateView, DeleteView

#extend views: you cannot combine views from the same group (base/display/edit groups)
#e.g. somethingView(CreateView, FormView) is bad!!, method inheritance is confusing.

from .models import Product, Comment, Category # . : in current directory

from .forms import ProductForm, CommentForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .permissions import IsOwnerOrReadOnly
@method_decorator(login_required, name = 'dispatch') #dispatch: find get/post method, restrict
class PostCreate(View):
    def get(self, request): #get the information in the form
        form = ProductForm
        return render(request, 'products/product_create.html', {'form': form})

    def post(self, request): #create a post
        form = ProductForm(request.POST)
        form.author = request.user #set author as the user
        if form.is_valid():
            form.save() #save the form
            return redirect(reverse('home')) #redirect to home
        #else:   
        return render(request, 'products/product_create.html', {'form': form}) #stay at the same page

@login_required
def product_update(request, id = id):
    product = get_object_or_404(Product, id = id)
    if product.author != request.user:
        return redirect(reverse('home')) #not authorised

    form = ProductForm(request.POST or None, instance= product)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "products/product_create.html", context)
class PageContextMixin():
    page_title = None #attribute to be overwritten

    def get_context_data(self, **kwargs):
        context = super(PageContextMixin, self).get_context_data(**kwargs) 
        context['page_title'] = self.page_title #add the page_title attribute to the context
        return context
        
def products_list(request):
    """
    Renders the polls_list.html template which lists all the
    currently available polls
    """
    products = Product.objects.get_queryset().order_by('id')
    search_term = '' #initialisation
    if 'title' in request.GET:
        products = products.order_by('title')

    if 'pub_date' in request.GET:
        products = products.order_by('-pub_date')

    if 'view_count' in request.GET:
        products = products.order_by('-view_count')

    if 'search' in request.GET:
        search_term = request.GET['search']
        products = products.filter(title__icontains=search_term)

    paginator = Paginator(products, 3)

    page = request.GET.get('page')
    products = paginator.get_page(page) #specific chunk of products

    #Preserving Query Parameters When Using Paginator
    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()

    context = {'posts': products, 'params': params, 'search_term': search_term}   
    return render(request, 'products/product_list.html', context)


class PostDisplay(SingleObjectMixin, View): #inherits from SingleObjectMixin View instead
    #SingleObjectMixin provides the ability to retrieve a single object for further manipulation
    model = Product #the context
    def get(self, request, *args, **kwargs): #override the get method from View
        self.object = self.get_object() #extends the SingleObjectMixin, SingleObjectMixin has access to the get_object function
        #override
        self.object.view_count +=1 #manipulate view_count
        self.object.save()

        listing = self.get_context_data(object = self.object)

        if request.user != self.object.author: #the person viewing is not the listing's author
            return render(request, 'products/product_detail_guest.html', listing) #this html hides the update and delete button

        return render(request, 'products/product_detail.html', listing)
    
    def get_context_data(self, **kwargs):
        '''
        insert the single object into the context dictionary
        '''
        #override
        context = super(PostDisplay, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(listing = self.get_object()) 
        #filter: filter out the comments that are for this post only

        #comment section for each post:
        context['form'] = CommentForm
        return context


@method_decorator(login_required, name = 'dispatch') 
class PostComment(FormView): #processing to receive the comment
    form_class = CommentForm
    template_name = 'products/product_detail.html'
    
    #override
    def form_valid(self, form):
        form.instance.author = self.request.user #set author as user
        product = Product.objects.get(pk = self.kwargs['pk']) #insert comment to current post
        form.instance.listing = product
        form.save() #remember to save the form!
        return super(PostComment, self).form_valid(form) #override

    def get_success_url(self): #redirect to this url if successful
        return reverse('product-detail', kwargs = {'pk': self.kwargs['pk']} )

@method_decorator(login_required, name = 'dispatch') 
class PostDetail(View):
    #combine two views
    #PostDetail is PostDisplay and PostComment combined
    
    #first view
    def get(self, request, *args, **kwargs):
        view = PostDisplay.as_view()
        return view(request, *args, **kwargs)
    
    #second view

    def post(self, request, *args, **kwargs):
        view = PostComment.as_view()
        return view(request, *args, **kwargs)

@login_required
def product_delete_view(request, id):
    product = get_object_or_404(Product, id= id)
    if product.author != request.user:
        return redirect(reverse('home')) #not authorised

    if request.method == "POST":
        product.delete()
        return redirect(reverse('home'))
    context = {
        "post": product
    }
    return render(request, "products/product_delete.html", context)

#filter by category
class PostCategory(ListView):
    model = Product
    template_name = 'products/product_category.html'
    def get_queryset(self): #override
        my_category = get_object_or_404(Category, pk = self.kwargs['pk']) #get category from url
        return Product.objects.filter(category = my_category) #filter by category
    
    def get_context_data(self, **kwargs):
        my_category = get_object_or_404(Category, pk = self.kwargs['pk']) #get category from url
        context = super(PostCategory, self).get_context_data(**kwargs)
        context["this_category"] = my_category #add category to context dictionary
        print(context)
        return context
