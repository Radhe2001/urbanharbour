from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Slider,User,Category,Brand,Product,Cart,Order
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your views here.
def index(request):
  if request.method == 'POST':
    query = request.POST.get('q')
    obj = Slider.objects.all()
    category = Category.objects.all()[:3]
    brand = Brand.objects.all()[:3]
    product = Product.objects.all()[:3]
    results = Product.objects.filter(name__contains=query)

    
    return render(request,'index.html',{"obj":obj,"category":category,"brand":brand,"product":product,"results":results})
  
  obj = Slider.objects.all()
  category = Category.objects.all()[:3]
  brand = Brand.objects.all()[:3]
  product = Product.objects.all()[:3]
  
  return render(request,'index.html',{"obj":obj,"category":category,"brand":brand,"product":product})


def brand_page(request):
  brand = Brand.objects.all()
  return render(request,'brand.html',{"brand":brand})

def category_page(request):
  category = Category.objects.all()
  return render(request,'category.html',{"category":category})
  
def product_page(request):
  product = Product.objects.all()
  return render(request,'product.html',{"product":product})

def offer_page(request):
  offer = Product.objects.filter(offer=True)
  return render(request,'offers.html',{"offer":offer})

def about(request):
  return render(request,'about.html')

def brand_detail(request,id):
  brand = Product.objects.filter(brand=id)
  return render(request,'brand_detail.html',{"detail":brand})

def category_detail(request,id):
  category = Product.objects.filter(category=id)
  return render(request,'category_detail.html',{"detail":category})


def detail(request,id):
  details = Product.objects.get(id=id)
  return render(request,'product_details.html',{"detail":details})

def user_login(request):
  
  user = request.COOKIES.get('isLoggedIn')
  if user=="yes":
    response = redirect("index")
    response.set_cookie('isLoggedIn', 'no')
    response.set_cookie('id', '', expires='Thu, 01 Jan 1970 00:00:00 GMT')
    return response 
  else:
    if request.method == 'POST':
      email = request.POST.get('email')
      password = request.POST.get('password')
      
      user = User.objects.filter(email=email, password=password)
      if len(user) == 1:
        response = redirect("index")
        response.set_cookie('isLoggedIn', "yes")
        response.set_cookie('id', user[0].id) 
        return response
  
  return render(request,'login.html')


def add_to_cart(request,id):
  logged_in = request.COOKIES.get('isLoggedIn')
  
  if logged_in:
    user = request.COOKIES.get('id')
    if user==None :
      details = Product.objects.get(id=id)
      return render(request,'product_details.html',{"detail":details})
      
    u_id = User.objects.get(id=user)
    p_id = Product.objects.get(id=id)
    instance = Cart.objects.create(product=p_id,user=u_id,count=1)
            
    details = Product.objects.get(id=id)
    return render(request,'product_details.html',{"detail":details,"added":True})
    
  details = Product.objects.get(id=id)
  return render(request,'product_details.html',{"detail":details})
  
def add_to_order(request,id):
  logged_in = request.COOKIES.get('isLoggedIn')
  
  if logged_in == 'yes':
    user = request.COOKIES.get('id')
    u_id = User.objects.get(id=user)
    p_id = Product.objects.get(id=id)
    total_price = Product.objects.get(id=id).discounted_price
    instance = Order.objects.create(product=p_id,user=u_id,count=1,total_price=total_price)
            
    details = Product.objects.get(id=id)
    return render(request,'product_details.html',{"detail":details,"ordered":True})
    
  details = Product.objects.get(id=id)
  return render(request,'product_details.html',{"detail":details})
  
  
  
def profile(request):
  id = request.COOKIES.get('id')
  if id == None :
    return redirect('index')
  else:
    obj = User.objects.get(id=id)
    return render(request,'profile.html',{"obj":obj})

def cart(request):
  id = request.COOKIES.get('id')
  if id == None :
    return redirect('index')
  else:
    c_items=[]
    obj = Cart.objects.filter(user=id)
    for o in obj:
      pr = Product.objects.get(id=o.product.id)
      c_items.append(pr)
    return render(request,'cart.html',{"obj":c_items})


def order(request):
  id = request.COOKIES.get('id')
  if id == None :
    return redirect('index')
  else:
    # return HttpResponse(id)
    obj = User.objects.get(id=id)
    return render(request,'profile.html',{"obj":obj})


def resize_image(image, width, height):
    if not image:
        return None

    img = Image.open(image)
    img_resized = img.resize((width, height), Image.ANTIALIAS)

    buffer = BytesIO()
    img_resized.save(buffer, format='JPEG')

    resized_image = InMemoryUploadedFile(
        buffer,
        None,  # field_name
        'profile_pic.jpg',  # file name
        'image/jpeg',  # content type
        buffer.tell(),  # size
        None  # content_type_extra
    )

    return resized_image



def register(request):
  
  if request.method == 'POST':
        # Accessing the uploaded file from the request.FILES
        uploaded_image = request.FILES.get('profile_pic')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        local_address = request.POST.get('local_address')
        town = request.POST.get('town')
        dist = request.POST.get('dist')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip = request.POST.get('zip')
        dob = str(request.POST.get('dob'))
        
        resized_image = resize_image(uploaded_image, 400, 400)

        if resized_image:
            instance = User(name=name,email=email,password=password,phone=phone,local_address=local_address,town=town,dist=dist,state=state,country=country,zip=zip,dob=dob,profile_pic=resized_image)
            instance.save()
            return redirect('index') 
  return render(request,'register.html')


