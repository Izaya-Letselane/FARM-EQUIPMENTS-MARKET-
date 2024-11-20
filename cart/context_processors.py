from .cart import Cart

#create context processor so that our cart can work in all pages

def cart(request):
    #return defaults cart data
    return {'cart': Cart(request)}