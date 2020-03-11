import os
import jwt
import datetime
import sql_model
from sanic_cors import CORS
from sanic import Sanic, response
from sanic.views import HTTPMethodView

app = Sanic(__name__)
CORS(app)

async def sign_up(request):
  if request.method == 'OPTIONS':
    return response.json({})
  
  data = request.json
  if not data:
    return response.json({'auth': False, 'message': 'Datos requeridos'}, 
      status=404)
  
  user_id = sql_model.save_user(data)
  if not user_id:
    return response.json({'auth': False, 
      'message': 'Correo electrónico registrado'}, status=404)

  token = jwt.encode({'id': user_id}, os.getenv('TOKEN_KEY'))
  return response.json({'auth': True, 'token': token, 
    'name': data.get('nombre')}, status=201)

async def login(request):
  if request.method == 'OPTIONS':
    return response.json({})
  
  data = request.json
  if not data:
    return response.json({'auth': False, 'message': 'Datos requeridos'}, 
      status=404)

  user = sql_model.get_user_email(data.get('correo'))
  if not user:
    return response.json({'auth': False, 'message': 'Usuario no encontrado'}, 
      status=401)

  if data.get('clave') != user[3]:
    return response.json({'auth': False, 
      'message': 'Clave o usuario inválido. Inténtalo de nuevo'}, status = 401)
  
  token = jwt.encode({'id': user[0]}, os.getenv('TOKEN_KEY'))
  return response.json({'auth': True, 'token': token, 
    'name': user[1]}, status=200)

def authorization(request):
  token = request.headers.get('Authorization')
  token = token.split(' ')[1]
  if not token:
    return None, response.json({'auth': False, 
      'message': 'No ha enviado un token'}, status=401)

  try:
    decoded = jwt.decode(token, os.getenv('TOKEN_KEY'), verify=True)
  except jwt.exceptions.DecodeError as e:
    print(e)
    return None, response.json({'auth': False, 'message': 'Token invalido'}, 
      status=401)

  return decoded, None

class CRTaskResource(HTTPMethodView):
  async def get(self, request):
    decoded, resp = authorization(request)
    if not decoded:
      return resp
    
    tasks = sql_model.get_tasks(decoded.get('id'))
    return response.json({'auth': True, 'tasks': tasks}, status=200)


  async def post(self, request):
    decoded, resp = authorization(request)
    if not decoded:
      return resp
  
    form_data = request.form
    img_file = request.files.get('imagen')
    if not form_data or not img_file:
      return response.json({'auth': True, 'message': 'Datos requeridos'}, 
        status=404)

    data = {
      'user_id': decoded.get('id'),
      'nombre_imagen': img_file.name[:30],
      'formato_imagen': img_file.type,
      'contenido_imagen': img_file.body,
      'nombre': form_data.get('nombre'),
      'descripcion': form_data.get('descripcion'),
      'fecha_creacion': datetime.datetime.now().isoformat(timespec='minutes')
    }
    task_id = sql_model.save_task(data)
    return response.json({'auth': True, 'create': task_id}, status=201)

  async def options(self, request):
    return response.json({})

class UDTaskResource(HTTPMethodView):
  async def put(self, request, _id):
    decoded, resp = authorization(request)
    if not decoded:
      return resp
  
    form_data = request.form
    img_file = request.files.get('imagen')
    if not form_data or not img_file:
      return response.json({'auth': True, 'message': 'Datos requeridos'}, 
        status=404)
    
    data = {
      'id': _id,
      'nombre': form_data.get('nombre'),
      'descripcion': form_data.get('descripcion'),
      'nombre_imagen': img_file.name[:30],
      'formato_imagen': img_file.type,
      'contenido_imagen': img_file.body
    }
    result = sql_model.update_entire_task(data)
    return response.json({'auth': True, 'updated': result}, status=200)
    
  async def patch(self, request, _id):
    decoded, resp = authorization(request)
    if not decoded:
      return resp

    form_data = request.form
    if not form_data:
      return response.json({'auth': True, 'message': 'Datos requeridos'}, 
        status=404)

    data = {
      'id': _id,
      'nombre': form_data.get('nombre'),
      'descripcion': form_data.get('descripcion')
    }
    result = sql_model.update_task_partially(data)
    return response.json({'auth': True, 'updated': result}, status=200)

  async def delete(self, request, _id):
    decoded, resp = authorization(request)
    if not decoded:
      return resp
    
    result = sql_model.delete_task(_id)
    return response.json({'auth': True, 'delete': result}, status=200)

  async def options(self, request, _id):
    return response.json({})

# Endpoints
app.add_route(login, '/login', ['POST', 'OPTIONS'])
app.add_route(sign_up, '/sign-up', ['POST', 'OPTIONS'])
app.add_route(CRTaskResource.as_view(), '/tasks')
app.add_route(UDTaskResource.as_view(), '/tasks/<_id>')

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000)