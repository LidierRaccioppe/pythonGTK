import sqlite3 as dbapi

columnas = ("Nombre", "Apellido", "Numero de teléfono")
agendaTelefonica = (
                    ("Pepe", "Pérez", "986 444 555"),
                    ("Ana", "Yañéz", "985 333 777"),
                    ("Roque", "Díz", "987 222 889"),
                    )
bbdd = dbapi.connect("baseTelefonica.dat")
# print(bbdd)
c = bbdd.cursor()
# print(c)
try:
    c.execute("""create table listaTelefonos (nombre text,
                               apellido text,
                               telefono integer)""")
except dbapi.DatabaseError as e:
    print("Error creando la tabla de listaTelefonos" + str(e))

try:
    for datos in agendaTelefonica:
        c.execute("""insert into listaTelefonos values(?, ?, ?)""", datos)
    bbdd.commit()
except dbapi.OperationalError as e:
    print("Error insertanto en la tabla de listaTelefonos" + str(e))

c.close()
bbdd.close()