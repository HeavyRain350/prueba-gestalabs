import json
import jwt
from db_functions import create_item,obtain_items_last_id

## Endpoint publico que regresa un hola mundo y que todos pueden ejecutar
def public(event, context):
    body = {
        "message": "Hello World!",
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

## Decorador del endpoint privado, para verificar si se lleva token jwt y si el token tiene la información solicitada
def authorizer(func):
    def wrapper(event, context):
        enc_jwt = json.loads(event["body"])['token']
        try:
            ## se trata de decodificar el token jwt con la llave
            dec_jwt = jwt.decode(enc_jwt, 'your-256-bit-secret', algorithms=["HS256"])

            ## se verifica la información del token
            if(dec_jwt['accessKey'] == 'QWERTYUIOP' and dec_jwt['role'] == 'bot'):

                ## una vez validado todo, se ejecuta el endpoint
                return func(event, context)
            else:
                ## en caso de que no la tenga, se manda un status de no autorizado para ejecutar el endpoint
                body = {
                    "message": "You are unauthorized to use this function!",
                }
                response = {"statusCode": 401, "body": json.dumps(body)}
                return response
        except jwt.exceptions.DecodeError:
            ## si el token es inválido para decodificarse con esa llave, se arroja un error 500
            body = {
                "message": "That is not a valid JWT token for the key!",
            }
            response = {"statusCode": 500, "body": json.dumps(body)}
            return response
    return wrapper

## Endpoint privado que inserta un item en la tabla items y regresa un status 200
@authorizer
def private(event, context):
    last_id = obtain_items_last_id()+1
    create_item(('item %d'%(last_id),))
    body = {
        "message": "The item %d last_id was created successfully!" %(last_id),
    }
    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

   
