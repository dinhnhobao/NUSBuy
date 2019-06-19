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

@method_decorator(login_required, name = 'dispatch') #dispatch: find get/post method, restrict
class PostCreate(View):
    def get(self, request): #get the information in the form
        form = ProductForm
        return render(request, 'products/product_create.html', {'form': form})

    def post(self, request): #create a post
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save() #save the form
            return redirect(reverse('home')) #redirect to home
        #else:   
        return render(request, 'products/product_create.html', {'form': form}) #stay at the same page

@method_decorator(login_required, name = 'dispatch') 
class PostUpdate(UpdateView):
    model = Product
    fields = ('image_link_1', 'image_link_2','image_link_3','image_link_4',
            'price_in_SGD', 'description', 'delivery_location', 'extra_information')
    template_name = 'products/product_create.html'

class PageContextMixin():
    page_title = None #attribute to be overwritten

    def get_context_data(self, **kwargs):
        context = super(PageContextMixin, self).get_context_data(**kwargs) 
        context['page_title'] = self.page_title #add the page_title attribute to the context
        return context
        
class Home(PageContextMixin, ListView): #Mixin should always come before ListView
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'posts'
    ordering = '-view_count' #sort by ...
    paginate_by = 3 #number of listings per page, use products/pagination_links.html
    page_title = 'NUSBuy - Listings' #overwrite PageContextMixin's page_title

@method_decorator(login_required, name = 'dispatch') 
class PostDisplay(SingleObjectMixin, View): #inherits from SingleObjectMixin View instead
    #SingleObjectMixin provides the ability to retrieve a single object for further manipulation
    model = Product #the context
    def get(self, request, *args, **kwargs): #override the get method from View
        self.object = self.get_object() #extends the SingleObjectMixin, SingleObjectMixin has access to the get_object function
        #override
        self.object.view_count +=1 #manipulate view_count
        self.object.save()

        listing = self.get_context_data(object = self.object)
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

@method_decorator(login_required, name = 'dispatch') 
class PostDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('home')

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
