from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin
from django.core.paginator import Paginator
from django.views import generic
from .models import GPU, CPU, Manufacturer, Product, ProductImage, ProductRating, CartItem
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse #for ajax possibly
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
import json

from goods.forms import OrderProductForm
from goods.forms import AddCPUForm

def index(request):
  """View function for home page of site."""
  
  #Generate counts of some of the main objects {{ url1 }}{{ url2 }}url1=product.cpu.get_absolute_url url2=product.gpu.get_absolute_url
  num_gpu = GPU.objects.all().count()
  
  #The 'all()' is implied by default.
  num_cpu = CPU.objects.count()
  
  context = {
    'num_gpu': num_gpu, 
    'num_cpu': num_cpu, 
  }
  
  #Render the HTML template index.html with the data in the context variable
  return render(request, 'index.html', context=context)

class GPUListView(generic.ListView):
  model = GPU
  paginate_by = 3
  context_object_name = 'gpu_list' # your own name for the list as a template name
  queryset = GPU.objects.all() #.filter(fullname__icontains='') #[:5] # Get 5 gpus containing name nvidia
  #template_name = 'gpus/gpu_list.html' # Specify your own template name/location
  
class GPUDetailView(generic.DetailView):
  model = GPU

class CPUListView(generic.ListView):
  model = CPU
  paginate_by = 3
  context_object_name = 'cpu_list' # your own name for the list as a template name
  queryset = CPU.objects.all() #filter(fullname__icontains='') # Get all the cpus
  #template_name = 'cpus/cpu_list.html' # Specify your own template name/location

class CPUDetailView(generic.DetailView):
  model = CPU
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    images_list = self.get_object().productimage_set.all()
    context['user_rating'] = ProductRating.objects.filter(product=self.get_object(), user=self.request.user).first() or 0
    #print(type(images_list[0].image))
    context['images'] = images_list
    return context

class ManufacturerListView(generic.ListView):
  model = Manufacturer
  paginate_by = 2
  context_object_name = 'manufacturer_list'
  queryset = Manufacturer.objects.all()
  template_name = 'goods/producer_list.html'
  
#class ManufacturerDetailView(generic.DetailView, MultipleObjectMixin):
#  model = Manufacturer
#  paginate_by = 2
#  #context_object_name = 'product_list'
#  template_name = 'goods/producer_detail.html'
#  def get_context_data(self, **kwargs):
#    # Call the base implementation first to get a context
#    #object_list = Product.objects.filter(producer=self.get_object())
#    object_list = self.get_object().product_set.all()
#    context = super(ManufacturerDetailView, self).get_context_data(object_list=object_list, product_list=object_list, **kwargs)
#    # Add in a QuerySet of all the products
#    #if 'product_set' in locals():
#    #context['product_list'] = object_list
#    return context

#class to insert list functionality into detailView
#this is needed for Manufacturer and Cart Detail view to list their products
#and their details
class DetailListView(DetailView):
  object_set_name = '' #to later overload and put new name on set
  #overload
  #3 ends third   to get list of objects with mixed in paginator and give it 
  #over to template
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    object_list = self.get_object_set() #self.get_object().product_set.all()
    context[self.context_object_name] = object_list
    context['page_obj'] = object_list
    context['is_paginated'] = True
    context['paginator'] = object_list.paginator
    return context

  #non overload
  #1 ends first   to get list of objects
  def get_my_queryset(self):
    queryset = getattr(self.get_object(), self.object_set_name).all()
    return None

  #overload
  #2 ends second   to get list of objects and add paginator to it
  def get_object_set(self):
    paginator = Paginator(self.get_my_queryset(), 2) #paginate_by
    page = self.request.GET.get('page')
    object_set = paginator.get_page(page)
    #product_set.paginator = paginator
    #print("debug !!!!!!!!!!!!!!!! " + str(paginator.page_range))
    return object_set
  
class ManufacturerDetailView(DetailListView):
  model = Manufacturer
  template_name = "goods/producer_detail.html"
  context_object_name = 'product_list'
  object_set_name = 'product_set' #possibly the name of the foreign key to show
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    print("debug !!!111111!!!!! " + str(type(context['product_list'])))
    return context
    
  def get_my_queryset(self):
    return self.get_object().product_set.all()
#class ManufacturerDetailView(DetailView):
#  model = Manufacturer
#  template_name = "goods/producer_detail.html"
#  context_object_name = 'product_list'
#  def get_context_data(self, **kwargs):
#    context = super(ManufacturerDetailView, self).get_context_data(**kwargs)
#    #self is Manufacturer class (or object?), 
#    object_list = self.get_product_set() #self.get_object().product_set.all()
#    context['product_list'] = object_list
#    context['page_obj'] = object_list
#    context['is_paginated'] = True
#    context['paginator'] = object_list.paginator
#    return context

#  def get_product_set(self):
#    queryset = self.get_object().product_set.all() 
#    paginator = Paginator(queryset, 2) #paginate_by
#    page = self.request.GET.get('page')
#    product_set = paginator.get_page(page)
#    #product_set.paginator = paginator
#    #print("debug !!!!!!!!!!!!!!!! " + str(paginator.page_range))
#    return product_set

#cart
#

class DetailUser(LoginRequiredMixin, DetailListView):
  model = User
  template_name = 'detail_user.html'
  context_object_name = 'cart_items'
  object_set_name = 'cartitem_set'
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    print("debug !!!111111!!!!! " + str(context))
    print ("debug !!!?????!! " + str(context['cart_items']))
    #for k, v in context['cart_items']:
    #  context['cart_items'][k] = v.product
    #  print("debug !!!!!!!!!!!! " + str(item.fullname))
    return context

  #self is View class
  #self.get_object is View class' class' object (in this case User's object)
  def get_my_queryset(self):
    print("debug !!!222222!!!!! " + str(type(self.get_object().cartitem_set.all())))
    return self.get_object().cartitem_set.all()
  
  def get_object(self):
    return get_object_or_404(User, pk=self.request.user.id)

class ListCart(PermissionRequiredMixin, ListView):
  permission_required = 'goods.can_see_items'
  model = CartItem
  paginate_by = 2
  context_object_name = 'cart_items'
  queryset = CartItem.objects.all().order_by('user')
  template_name = 'list_carts.html'

#class ListCart(ListView):
#  model = Cart
#  context_object_name = 'carts'
#  template_name = 'cart/list_carts.html'
#  def get_context_data(self, **kwargs):
#    context = super().get_context_data(**kwargs)
#    print("debug !!!!!!!!!!!! " + str(context))
#    return context

#class CreateCart(CreateView):
#  model = Cart
#  template_name = 'cart/create_cart.html'

#class UpdateCart(UpdateView):
#  model = Cart
#  template_name = 'cart/update_cart.html'

#class DeleteCart(DeleteView):
#  model = Cart
#  template_name = 'cart/delete_cart.html'

##cartItem
##

#class DetailCartItem(DetailView):
#  model = CartItem
#  template_name = 'cartitem/detail_cartitem.html'

#class ListCartItem(ListView):
#  model = CartItem
#  context_object_name = 'cartitems'
#  template_name = 'cartitem/list_cartitems.html'

#class CreateCartItem(CreateView):
#  model = CartItem
#  template_name = 'cartitem/create_cartitem.html'

#class UpdateCartItem(UpdateView):
#  model = CartItem
#  template_name = 'cartitem/update_cartitem.html'

#class DeleteCartItem(DeleteView):
#  model = CartItem
#  template_name = 'cartitem/delete_cartitem.html'

def order_product(request, pk):
  product = get_object_or_404(Product, pk=pk)
  user = request.user
  cartitem = None
  
  # If this is a POST then process the Form data
  if request.method == 'POST':
    
    # Create a form instance and populate it with data from the request (binding):
    form = OrderProductForm(request.POST)
    
    # Check if the form is valid:
    if form.is_valid():
      # process the data in form.cleaned_data as required (here we just write it to the model)
      #debug to add
      #product.
      cartitem = CartItem()
      cartitem.product = product
      cartitem.user = user
      cartitem.quantity = form.cleaned_data['count']
      cartitem.save()
      
      # redirect to a new url
      return HttpResponseRedirect(reverse('user-detail'))
  
  # If this is a GET (or any other method) create the default form.
  else:
    form = OrderProductForm(initial={'count': 1})
  
  context = {
    'form': form, 
    'cartitem': cartitem, 
    'product': product, 
    'user': user
  }
  
  return render(request, 'goods/product_order.html', context)

def add_cpu(request):
  is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
  if request.method == 'POST' and is_ajax:
    form = AddCPUForm(request.POST)
    if form.is_valid():
      print("not valid")
    cpu = CPU()
    cpu.fullname = form.cleaned_data['name']
    cpu.price = form.cleaned_data['price']
#    cpu.fullname = request.POST.get('name')
#    cpu.price = request.POST.get('price')
    print("!!!!!!!!!!!!!!!!!!!!!request")
    #print(request.POST.dict())
    print(request.POST.dict())
    print(request.POST)
    print(form.errors.as_data())
    print(request.POST.get('name', None))
    print(form.cleaned_data['name'])
    #print(json.load(request))
#    print(json.loads(request.POST.get('price')))
#    print(cpu.fullname)
#    print(cpu.price)
    print("!!!!!!!!!!!!!!")
    cpu.save()
    images = request.FILES.getlist('files[]')
    if images:
      print("file here")
      for i in images:
        productimage = ProductImage()
        productimage.product = cpu
        productimage.image = i
        productimage.save()
    else:
      print("NO FILE AT ALL")
    return JsonResponse({'answer': 'answer1'})
#    else:
#      print("not valid")
#      return JsonResponse({'answer': 'fail1'})
  else:
    return render(request, "goods/addcpu.html")
  
#def add_cpu(request): #function for admin to add cpu to the db
#  if request.method == 'POST':
#    form = AddCPUForm(request.POST, request.FILES)
#    if form.is_valid():
#      cpu = CPU()
#      cpu.fullname = form.cleaned_data['name']
#      cpu.price = form.cleaned_data['price']
#      cpu.save()
#      images = request.FILES.getlist('images')
#      if images:
#        for i in images:
#          productimage = ProductImage()
#          productimage.product = cpu
#          productimage.image = i
#          productimage.save()
#  else:
#    form = AddCPUForm()
#  context = {'form': form, }
#  return render(request, "goods/addcpu.html", context)

def rate(request, product_id, rating): #api function
  product = Product.objects.get(pid=product_id)
  ProductRating.objects.filter(product=product, user=request.user).delete()
  product.productrating_set.create(user=request.user, rating=rating)
  print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  print("rating")
  url = "goods/cpu/" + str(product_id)
  return HttpResponse("") #do not know why it is requiered to return seemingly a webpage in an API function
#function for admin to add photos to cpu or gpu or other product
#def add_product_photo(request, pk):
#  product = get_object_or_404(Product, pk=pk)
#  if request.method == 'POST':
#    form = AddCPUForm(request.POST, request.FILES)
#    if form.is_valid():
#      images = request.FILES.getlist('images')
#      if form.is_valid():
#        for i in images:
#          productimage = ProductImage()
#          productimage.product = product
#          productimage.image = i
#          productimage.save()
#  else:
#    form = AddCPUForm()
#  context = {'form': form, }
#  return render(request, "goods/addcpu.html", context)

