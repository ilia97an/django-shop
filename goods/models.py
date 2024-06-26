from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
from django.db.models import Avg
import inspect

#meta classes
#

class ShopItemMeta(models.Model):
  pid = models.BigAutoField(primary_key=True)
  fullname = models.CharField(max_length=120, blank=True, null=True)
  description = models.TextField(blank=True, null=True)
  class Meta:
    abstract = True

class ProductMeta(ShopItemMeta):
  producer = models.ForeignKey('Manufacturer', on_delete=models.SET_NULL, null=True, blank=True, related_name='product_set')
  price = models.IntegerField(blank=True, null=True) #tenne
  class Meta:
    abstract = True
  def average_rating(self):
    return ProductRating.objects.filter(product=self).aggregate(Avg("rating"))["rating__avg"] or 0
    
  def price_str(self):
    string = ""
    if not self.cpu.price is None:
      string = str(int(self.price / 100)) + "." + "{:02d}".format(self.price % 100) + " TMT"
    return string
    
  def get_absolute_url(self):
    """Return the URL to access a particular product instance."""
    urlnames = ['cpu', 'gpu']
    urlname = ''
    #print("debug !!!!!!!!!!!!!!! " + str(inspect.getmembers(self)))
    #this is method of product, hence it contains not the gpu's or cpu's
    #attributes, but link to gpu or cpu
    #somehow somewhat kind of....
    for u in urlnames:
      if hasattr(self, u):
        urlname = u
        break
    return reverse(urlname + "-detail", args=[str(self.pid)])

#database classes
#

class Product(ProductMeta):
  pass

class ProductImage(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  image = models.ImageField(upload_to='images/', blank=True, null=True)

class ProductRating(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  rating = models.IntegerField(default=0)
  def __str__(self):
    return f"{self.product.fullname}: {self.rating}"

class Manufacturer(ShopItemMeta):
  def get_absolute_url(self):
    """Return the URL to access a particular manufacturer instance."""
    return reverse('producer-detail', args=[str(self.pid)])
  def __str__(self):
    """String for representing the Manufacturer object."""
    return self.fullname

#shop cart
#

class CartItem(models.Model):
  class Meta:
    permissions = (("can_see_items", "Permission for salesmen"), )
  pid = models.BigAutoField(primary_key=True)
  #the distant object that is linked to this object will be able to have many
  #links to the objects of this class
  product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True)#BigAutoField(blank=True, null=True) #ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True)
  #the cart (as container of ordered products)/db-record will not be created
  #and cart items will belong to the user directly
  user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
  quantity = models.IntegerField(default=1, blank=True, null=True)

#different kinds of products
#

class GPU(Product, ProductMeta):
  ramtype = models.CharField(max_length=60, blank=True, null=True)
  ramwidth = models.IntegerField(blank=True, null=True)
  ramclock = models.IntegerField(blank=True, null=True)
  endmanufacturer = models.CharField(max_length=60, blank=True, null=True)
  clock = models.IntegerField(blank=True, null=True) #megaherz
  tdp = models.IntegerField(blank=True, null=True)
  architecture = models.CharField(max_length=60, blank=True, null=True)
  def get_absolute_url(self):
    """Returns the URL to access a detail record for this gpu."""
    return reverse('gpu-detail', args=[str(self.pid)])

class CPU(Product, ProductMeta):
  clock = models.IntegerField(blank=True, null=True) #megaherz
  cores = models.IntegerField(blank=True, null=True)
  tdp = models.IntegerField(blank=True, null=True)
  architecture = models.CharField(max_length=60, blank=True, null=True)
  def get_absolute_url(self):
    """Returns the URL to access a detail record for this cpu."""
    return reverse('cpu-detail', args=[str(self.pid)])

