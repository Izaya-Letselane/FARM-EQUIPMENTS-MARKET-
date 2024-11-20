from ecomm.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        
        #get the current key if it exists
        cart = self.session.get('session_key')
        #check if user is new, no session key, Create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        #make cart available in all pages
      
        self.cart = cart
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        #Work on logged in user
        if self.request.user.is_authenticated:
            #obtain curr user prof
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #use json, to convert {'4': 2} to {"4": 2}
            cartConv =  str(self.cart) #"{'4:'3}" it's now a string"
            cartConv = cartConv.replace("\'", "\"")
            #save cartconv to the Profile model
            current_user.update(prev_card=str(cartConv))
        
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        #Work on logged in user
        if self.request.user.is_authenticated:
            #obtain curr user prof
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #use json, to convert {'4': 2} to {"4": 2}
            cartConv =  str(self.cart) #"{'4:'3}" it's now a string"
            cartConv = cartConv.replace("\'", "\"")
            #save cartconv to the Profile model
            current_user.update(prev_card=str(cartConv))
    
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()
        
        products = Product.objects.filter(id__in=product_ids)
        
        return products
    def get_quants(self):
        quantities= self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        
        #get cart
        ourcart = self.cart
        #update cart dictionary
        ourcart[product_id] = product_qty
        self.session.modified = True
        
        
        #handling login user persistence
        if self.request.user.is_authenticated:
            #obtain curr user prof
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #use json, to convert {'4': 2} to {"4": 2}
            cartConv =  str(self.cart) #"{'4:'3}" it's now a string"
            cartConv = cartConv.replace("\'", "\"")
            #save cartconv to the Profile model
            current_user.update(prev_card=str(cartConv))
        thing = self.cart
        return thing
    def delete(self, product):
        product_id = str(product)
        #delete from dictionary
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True
        if self.request.user.is_authenticated:
            #obtain curr user prof
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #use json, to convert {'4': 2} to {"4": 2}
            cartConv =  str(self.cart) #"{'4:'3}" it's now a string"
            cartConv = cartConv.replace("\'", "\"")
            #save cartconv to the Profile model
            current_user.update(prev_card=str(cartConv))
            
    def cart_total(self):
        #get product ids
        product_ids = self.cart.keys()
        #look keys in database model
        products = Product.objects.filter(id__in=product_ids)
        #Get quantities
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            #convert key string into int to perform math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
                        
        
        return total