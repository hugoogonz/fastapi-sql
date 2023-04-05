from config.database import Base
from sqlalchemy import Column, Integer, String, Float

#  La clase Movie representa una tabla llamada "movies" en la base de datos
class Movie(Base):
    # El atributo __tablename__ se establece en "movies" para indicar que esta clase representa la tabla "movies" en la base de datos
    # Con esta clase, se pueden realizar consultas y operaciones CRUD en la tabla "movies" utilizando una instancia de la clase Session de SQLAlchemy
    __tablename__ = "movies"

    # Las columnas se definen utilizando los objetos Column del módulo sqlalchemy
    # La función Column acepta dos argumentos: el tipo de datos de la columna y, opcionalmente, una serie de argumentos de configuración adicionales
    # La opción primary_key=True se utiliza para indicar que la columna id es la clave primaria de la tabla.
    id = Column(Integer, primary_key = True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)