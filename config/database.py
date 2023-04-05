"""
Este código importa varios módulos y crea una instancia de la base declarativa de SQLAlchemy para definir las clases que representarán las tablas de la base de datos.

"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Se establece el nombre del archivo de la base de datos y se crea una URL de conexión con la base de datos SQLite. 
sqlite_file_name = "database.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__))

# La URL de conexión se utiliza para conectarse a la base de datos y crear el motor de la base de datos.
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

# create_engine es una función de SQLAlchemy que crea una conexión con la base de datos.
engine = create_engine(database_url, echo=True)

# sessionmaker es una función de SQLAlchemy que crea una clase de sesión que se puede usar para interactuar con la base de datos.
# Finalmente, se crea una clase Session que se puede usar para interactuar con la base de datos, y se crea una clase base Base para las definiciones de clase de SQLAlchemy. 
# Con estas clases, se pueden definir las tablas y las relaciones de la base de datos en una forma orientada a objetos.
Session = sessionmaker(bind=engine)

# declarative_base es una función de SQLAlchemy que crea una clase base para las definiciones de clase de SQLAlchemy.
Base = declarative_base()