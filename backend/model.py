import os
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
def get_user_id(conn, user_id):
  cursor = conn.cursor() 
  sql = """SELECT * FROM USER WHERE id = '{}'""".format(user_id)
  result = None

  try:
    cursor.execute(sql)
    result = cursor.fetchone()
  except Exception as e:
    print(e)

  return result

@decorator_conn
def get_user_email(conn, email):
  cursor = conn.cursor() 
  sql = """SELECT * FROM USER WHERE correo = '{}'""".format(email)
  result = None

  try:
    cursor.execute(sql)
    result = cursor.fetchone()
  except Exception as e:
    print(e)

  return result

@decorator_conn
def save_user(conn, user):
  cursor = conn.cursor()
  user_id = str(uuid4())
  sql = """INSERT INTO USER (id, nombre, correo, clave, fecha_nacimiento, 
    genero) VALUES ('{}','{}', '{}', '{}', '{}', '{}')""".format(user_id, 
    user.get('nombre'), user.get('correo'), user.get('clave'), 
    user.get('fecha_nacimiento'), user.get('genero'))
  result = None

  try:
    cursor.execute(sql)
    conn.commit()
    result = user_id
  except Exception as e:
    print(e)

  return result

@decorator_conn
def get_tasks(conn, user_id):
  cursor = conn.cursor()
  sql = """SELECT * FROM TAREA WHERE user_id = '{}'""".format(user_id)
  result = []

  try:
    cursor.execute(sql)
    for item in cursor.fetchall():
      result.append(list(item))
  except Exception as e:
    print(e)
  
  return result

@decorator_conn
def save_task(conn, task):
  cursor = conn.cursor()
  task_id = str(uuid4())
  sql = """INSERT INTO TAREA (id, user_id, nombre, descripcion, 
    fecha_creacion, nombre_imagen) 
    VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
    """.format(task_id, task.get('user_id'), task.get('nombre'), 
    task.get('descripcion'), task.get('fecha_creacion'), 
    task.get('nombre_imagen'))
  result = None

  try:
    cursor.execute(sql)
    conn.commit()
    result = task_id
  except Exception as e:
    print(e)
  
  return result

@decorator_conn
def update_task(conn, task):
  cursor = conn.cursor()
  sql = """UPDATE TAREA SET nombre = '{}', descripcion = '{}', 
    nombre_imagen = '{}' WHERE TAREA.id = '{}'""".format(task.get('nombre'), 
    task.get('descripcion'), task.get('nombre_imagen'), task.get('id'))
  result = None

  try:
    cursor.execute(sql)
    conn.commit()
    result = cursor.rowcount
  except Exception as e:
    print(e)
  
  return result

@decorator_conn
def delete_task(conn, task_id):
  cursor = conn.cursor()
  sql = """DELETE FROM TAREA WHERE id = '{}'""".format(task_id)
  result = None

  try:
    cursor.execute(sql)
    conn.commit()
    result = cursor.rowcount
  except Exception as e:
    print(e)
  
  return result

if __name__ == "__main__":
  """ _id = save_task({
    'user_id': 'a30f7847-668e-44b3-9e2b-416934866623',
    'nombre': 'trabajo',
    'descripcion': 'hacer el trabajo de matemáticas',
    'fecha_creacion': '2020-02-21',
    'imagen': 'jalsdfj'
  })
  print(_id) """
  """ 
  print(get_tasks('a30f7847-668e-44b3-9e2b-416934866623'))
  print()
  print(update_task({
    'id': 'dd40a414-7eea-4011-9d9c-7aac86e91a2b',
    'nombre': 'trabajo de grado',
    'descripcion': 'hacer el trabajo ',
    'fecha_creacion': '2020-02-20',
    'imagen': 'jalsdfjppp'
  }))
  print() """
  
  #print(delete_task('1ce279a0-5685-4e13-b982-e43486c49a2c'))
  
  print(get_user_email('daniel@gmail.co'))
















