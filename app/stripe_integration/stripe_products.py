import stripe

from pydantic import BaseModel
from pydantic import  ValidationError

import os
from dotenv import load_dotenv

env_path = os.path.join(".", ".env")
load_dotenv(dotenv_path=env_path)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


import stripe

async def get_payment_links():
    try:
        payment_links = stripe.PaymentLink.list(limit=100, active=True)
        links = [link.url for link in payment_links.data]
        productos = [producto.name for producto in stripe.Product.list(limit=100).data]

        print("links", links)
        print("productos", productos)
        print("_______________________________________________")
        productos_invertidos = productos[::-1]
        print("productos_invertidos", productos_invertidos)

        print("**********************************************")
        print("links invertidos [::-1]", links[::-1])
        links_invertidos = links[::-1]

        links_y_productos = dict(zip(links, productos_invertidos))
        print("**********************************************")
        print("links y productos", links_y_productos)

        return links_y_productos, productos

    except Exception as e:
        print(f"Error: {e}")
        return None, None



#     ### Get Payment Links ###
# async def get_payment_links():
#         try:
#             payment_links = stripe.PaymentLink.list(limit=100, active=True)
#             # print("payment_links", payment_links.data[1].url)
#             productos = stripe.Product.list(limit=100).data
  
#             templist = []
#             for i in payment_links.data:
#                 templist.append(i.url)   
#             print("links",templist)
#             links = templist
#             templist2 = []
#             for j in range(len(productos)):
#                 li = productos[j].name
#                 templist2.append(li)
                
#             print("productos",templist2)
#             print("_______________________________________________")
#             print("productos_invertidos",list.reverse(templist2))
#             productos = templist2
            
#             print("**********************************************")
#             print("links", links)
#             print("links invertidos [::-1]", list(links[::-1]))
#             links_invertidos = list(links[::-1])
#             links_y_productos = {}
#             linarray = [i for i in range(1, len(links)+1)]
#             print("////////////////////////////////////////////////")
#             print(linarray)
#             shift_linarray = [i-1 for i in linarray]
#             print("////////////////////////////////////////////////")
#             print("shift_linarray", shift_linarray) 
#             shift_productos = [productos[i-2] for i in shift_linarray]
#             print("////////////////////////////////////////////////")
#             print("shift_productos",shift_productos[::1])
#             productos_invertidos = shift_productos[::1]
#             links_y_productos = dict(zip(links, productos_invertidos))
#             print("**********************************************")
#             print("links y productos", links_y_productos)
        
      
#             # productos = list.reverse(productos)
#             # for index, link in enumerate(payment_links.data):
#             #     producto = productos_invertidos[index]
#             #     links_y_productos[link.url] = producto.name
#             return links_y_productos

#         except Exception as e:
#             return {"error": str(e)}
            
