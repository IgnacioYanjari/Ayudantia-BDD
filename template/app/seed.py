from config import *
import psycopg2

conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,password))
cur = conn.cursor()

# Crear categorias
categorias = [ 'Tecnologia', 'Video Juegos', 'Geek', 'Cine', 'Mundo Marvel'];

for categoria in categorias :
    sql = """ insert into categorias (nombre, creado) values ('%s', now());"""%(categoria)
    cur.execute(sql)
    conn.commit()

# Crear posts para usuario id = 1
posts = [
(1, 'Doctor Strange','El men que viaja en el tiempo',
'Esta pelicula bla bla bla y es la mejor por que si '),
(1, 'Spiderman','Se retira el MEN',
'Esta pelicula bla bla bla ')
]

for post in posts :
    sql ="""
    insert into posts (usuario_id,titulo,resumen,texto,creado) values (%i,'%s','%s','%s',now())
    returning id;"""%(post);
    cur.execute(sql)
    conn.commit()

# Obtener todos los posts
sql = """select id from posts;"""
cur.execute(sql)
posts_id = cur.fetchall()

# Asignar categorias a cada post
for post_id in posts_id :
    post_id = post_id[0]
    # Se asignaran Mundo marvel, geek y cine
    sql= """SELECT id  FROM categorias where nombre = 'Cine' or
     nombre = 'Geek' or nombre = 'Mundo Marvel';"""
    cur.execute(sql)
    selected_categories = cur.fetchall()

    # insertar en relacion n:m
    for selected in selected_categories :
        category_id = selected[0]
        sql = """insert into categorias_posts (categoria_id, post_id)
        values('%i','%i');"""%(category_id, post_id)
        cur.execute(sql)
        conn.commit()


sql ="""insert INTO usuarios (nombre,apellido,email,passwd,creado)
 values ('Ignacio','Yanjari','ignacio.yanjari@mail.udp.cl','1234',now() );
"""

cur.execute(sql)
conn.commit()

cur.close()
conn.close()
