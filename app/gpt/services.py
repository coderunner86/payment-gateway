import httpx
from fastapi import HTTPException, Request
from app.settings.database import database
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from app.user.services import UserService
from app.stripe_integration.stripe_products import get_payment_links
load_dotenv()

class UserQuestion(BaseModel):
    question: str
    userId: Optional[int] = None
    
API_KEY = os.getenv("API_KEY")

class GptService:
    def __init__(self):
        self.API_KEY = API_KEY
        self.repository = database

    async def ask_gpt(self, question: str) -> str:
        async with httpx.AsyncClient() as client:
            try:
                    products = await client.get('http://localhost:8000/api/products/all_products', headers={
                        'Content-Type': 'application/json',
                        'Application': 'application/json'
                    }) 
                    products.raise_for_status()
                    products_json = products.json()
                    product_descriptions = ", ".join([f"{product['name']}: {product['description']}" for product in products_json])
                    delimiter = "####"
                    payment_links = await get_payment_links()
                    buy_links = ""
                    for link, titulo, recursos, descripcion in payment_links:
                        buy_links += f"Título: {titulo}\nDescripción: {descripcion}\nEnlace de Pago: {link}\nRecursos Adicionales: {', '.join(recursos)}\n\n"
                    

                    system_messages = f"""
                    Sigue estos pasos para responder a las consultas de los clientes.
                    La consulta del cliente estará delimitada por cuatro almohadillas,\
                    es decir, {delimiter}.

                    Paso 1:{delimiter} Primero decide si el usuario está \
                    haciendo una pregunta sobre un producto o productos específicos. \
                    La categoría del producto no cuenta.

                    Paso 2:{delimiter} Si el usuario pregunta sobre \
                    productos específicos, identifica si \
                    los productos están en la siguiente lista.
                    Todos los productos disponibles: 
                    {product_descriptions} 

                    Paso 3:{delimiter} Si el mensaje contiene productos \
                    en la lista anterior, ofrece el enlace de pago del producto\
                    que tiene el mismo nombre en {buy_links} .

                    Paso 4:{delimiter}: Si el usuario hizo alguna suposición, \
                    averigua si la suposición es cierta basada en tu \
                    información del producto o en lo que hay en {buy_links} \
                    
                    Paso 5:{delimiter}: Si el usuario no está preguntando por libros\
                    específicos ofrece un producto de compra de lo que hay en {buy_links}.

                    Paso 6:{delimiter}: Primero, corrige cortésmente las \
                    suposiciones incorrectas del cliente si corresponde. \
                    Solo menciona o referencia productos en la lista de \
                    productos disponibles, ya que estos son los únicos \
                    productos que vende la tienda. \
                    Responde al cliente en un tono amigable.

                    Utiliza el siguiente formato:
                    Paso 1:{delimiter} <razonamiento del paso 1>
                    Paso 2:{delimiter} <razonamiento del paso 2>
                    Paso 3:{delimiter} <razonamiento del paso 3>
                    Paso 4:{delimiter} <razonamiento del paso 4>
                    Respuesta al usuario:{delimiter} <respuesta al cliente>

                    Asegúrate de incluir {delimiter} para separar cada paso.
                    """
                    user_messages = f"""
                    {question}"""

                    messages = [  
                        {'role': 'system', 
                        'content': system_messages},    
                        {'role': 'user', 
                        'content': f"{delimiter}{user_messages}{delimiter}"},  
                    ]
                    prompt = ""
                    for message in messages:
                        prompt += f"{message['role'].title()}: {message['content']}\n"
                    response = await client.post(
                        'https://api.openai.com/v1/engines/gpt-3.5-turbo-instruct/completions',
                        headers={
                            'Authorization': f'Bearer {self.API_KEY}',
                            'Content-Type': 'application/json',
                        },
                        
                        json={
                             'prompt':prompt,
                            'temperature': 0.7,
                            'max_tokens': 500,
                        }
                    )
                    response.raise_for_status()
                    return response.json()['choices'][0]['text']
            except httpx.RequestError as e:
                    raise HTTPException(status_code=400, detail=f"HTTP request failed: {e}")

    async def create_question(self, request: Request, userquestion: UserQuestion):
        try:
            # Obtener el user_id de la sesión
            values = request.cookies.get("session_id")
            values = values.strip("() ")
            values = (values).split(",").pop(1)
            
            user_id = int(values)

            print("user_id", user_id)
           
            # Obtener la respuesta de GPT-3
            gptResponse = await self.ask_gpt(userquestion.question)
            data = userquestion.dict()
            
            data['userId'] = user_id  

            # Almacenar la pregunta 
            result = await self.repository.userquestion.create(data=data)
        
            find_the_user = await UserService().find_user(user_id=user_id)
            
            email = find_the_user.email
            name = find_the_user.name
            password = find_the_user.password
            gptResponse = gptResponse
    
            user_data={
                "name": name,
                "email": email,
                "password": password,
                "gptResponse": gptResponse
                }
            print("data_user", user_data)
            # Almacenar la respuesta 
            update_user = await self.repository.user.update(where={"id": user_id},
                data=user_data)
          
            return gptResponse
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail=f"Error creating question: {e}")

    