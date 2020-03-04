import os
import base64
import dotenv
import pymysql
from uuid import uuid4

dotenv.load_dotenv()

config = {
  'host': os.getenv('HOST'),
  'user': os.getenv('USER_DB'),
  'password': os.getenv('PASSWORD'),
  'db': os.getenv('DB')
}

def decorator_conn(func):
  """Decorador para abrir y cerrar la conexión con la base de datos.

    El decorador es una función que da la posibilidad de ejecutar cosas antes 
    o después de ejecutar la función que recibe como parametro

    Parametros:
    func : función
        función que realiza las consultas a la base de datos

    Retorna:
    open_close_conn : function
        función que abre y cierra la conexion con la base de datos
    
    Nota:
    result : es el resultado de ejecutar la función func
    *args: comodín que pasa n argumentos como una tupla
    **kwargs: comodín que pasa n argumentos con clave: valor
    """
  def open_close_conn(*args, **kwargs):
    conn = connection()
    result = func(conn, *args, **kwargs)
    conn.close()
    return result
  return open_close_conn

def connection():
  conn = None
  try:
    conn = pymysql.connect(
      host = config.get('host'),
      user = config.get('user'),
      password = config.get('password'),
      db = config.get('db')
    )
  except Exception as e:
    print(e)
  
  return conn

@decorator_conn
def get_user_email(conn, email):
  cursor = conn.cursor() 
  sql = """SELECT * FROM USER WHERE correo = %s"""
  data_tuple = (email,)
  result = None

  try:
    cursor.execute(sql, data_tuple)
    result = cursor.fetchone()
  except Exception as e:
    print(e)

  return result

@decorator_conn
def save_user(conn, user):
  cursor = conn.cursor()
  user_id = str(uuid4())
  sql = """INSERT INTO USER (id, nombre, correo, clave, fecha_nacimiento, 
    genero) VALUES (%s,%s, %s, %s, %s, %s)"""
  data_tuple = (user_id, user.get('nombre'), user.get('correo'), 
    user.get('clave'), user.get('fecha_nacimiento'), user.get('genero'))
  result = None

  try:
    cursor.execute(sql, data_tuple)
    conn.commit()
    result = user_id
  except Exception as e:
    print(e)

  return result

@decorator_conn
def get_tasks(conn, user_id):
  cursor = conn.cursor()
  sql = """SELECT * FROM TAREA WHERE user_id = %s"""
  data_tuple = (user_id,)
  result = []

  try:
    cursor.execute(sql, data_tuple)
    for item in cursor.fetchall():
      item = list(item)
      base64_encoded_data = base64.b64encode(item[5])
      item[5] = 'data:'+item[7]+';base64,'+ base64_encoded_data.decode('utf-8')
      result.append(item)
      
  except Exception as e:
    print(e)
  
  return result

@decorator_conn
def save_task(conn, task):
  cursor = conn.cursor()
  task_id = str(uuid4())
  sql = """INSERT INTO TAREA (id, user_id, nombre, descripcion, 
    fecha_creacion, contenido_imagen, nombre_imagen, formato_imagen) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
  data_tuple = (task_id, task.get('user_id'), task.get('nombre'), 
    task.get('descripcion'), task.get('fecha_creacion'), 
    task.get('contenido_imagen'), task.get('nombre_imagen'), 
    task.get('formato_imagen'))
  result = None

  try:
    cursor.execute(sql, data_tuple)
    conn.commit()
    result = task_id
  except Exception as e:
    print(e)
  
  return result

@decorator_conn
def update_entire_task(conn, task):
  cursor = conn.cursor()
  sql = """UPDATE TAREA SET nombre = %s, descripcion = %s, 
    contenido_imagen = %s, nombre_imagen = %s, formato_imagen = %s 
    WHERE TAREA.id = %s"""
  data_tuple = (task.get('nombre'), task.get('descripcion'), 
    task.get('contenido_imagen'), task.get('nombre_imagen'), 
    task.get('formato_imagen'), task.get('id'))
  result = None

  try:
    cursor.execute(sql, data_tuple)
    conn.commit()
    result = cursor.rowcount
  except Exception as e:
    print(e)
  
  return result

@decorator_conn
def update_task_partially(conn, task):
  cursor = conn.cursor()
  sql = """UPDATE TAREA SET nombre = %s, descripcion = %s 
    WHERE TAREA.id = %s"""
  data_tuple = (task.get('nombre'), task.get('descripcion'), task.get('id'))
  result = None

  try:
    cursor.execute(sql, data_tuple)
    conn.commit()
    result = cursor.rowcount
  except Exception as e:
    print(e)
  
  return result

@decorator_conn
def delete_task(conn, task_id):
  cursor = conn.cursor()
  sql = """DELETE FROM TAREA WHERE id = %s"""
  data_tuple = (task_id,)
  result = None

  try:
    cursor.execute(sql, data_tuple)
    conn.commit()
    result = cursor.rowcount
  except Exception as e:
    print(e)
  
  return result
