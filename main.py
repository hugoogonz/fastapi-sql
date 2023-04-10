from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
# JSONResponse me permite enviar contenido en formato JSON hacia el cliente
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder
# me permite crear el esquema de datos
from pydantic import BaseModel, Field
from typing import Optional, List

from jwtmanager import create_token, validate_token
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel

app = FastAPI()

app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"

# La línea de código Base.metadata.create_all(bind=engine) crea todas las tablas definidas en las clases que heredan de la clase base Base en la base de datos. 
# La función create_all de la propiedad metadata de la clase Base es responsable de crear las tablas en la base de datos.

# El argumento bind se utiliza para especificar el motor de la base de datos que se va a utilizar para crear las tablas. 
# En este caso, se utiliza el motor engine que fue creado previamente con la función create_engine de SQLAlchemy.
# Esta línea de código es necesaria para crear todas las tablas definidas en las clases que heredan de la clase base Base en la base de datos
# Almacenar y trear datos de la tablar
Base.metadata.create_all(bind=engine) 


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@admin.com":
            raise HTTPException(status_code=403, detail="The credentials are invalid")

# Modelo que me permita añadir info al usuario
class User(BaseModel):
    email: str = Field(min_length=5, max_length=15)
    password: str = Field(min_length=5, max_length=15)


class Movie(BaseModel):
    id: Optional[int] = None  # campo opcional
    title: str = Field(min_length=5, max_length=45)  # campo maximo de 15 digitos
    overview: str = Field(min_length=15, max_length=250)
    year: int = Field(le=2025) # menor a 2025
    rating:float = Field(default=10, ge=1, le=10)
    category:str = Field(default='Categoria', min_length=5, max_length=15)
    
	# Clase donde añado una propiedad llamada schema_extra
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Avatar",
                "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
                "year": "2009",
       	 		"rating": 7.8,
        		"category": "Accion"
			}
		}


movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Accion"
    },
    {
        "id": 2,
        "title": "Lalaland",
        "overview": "Mia & Sebastian...",
        "year": "2016",
        "rating": 10,
        "category": "Romantico"
    }
]


@app.get('/', tags=['home'])
async def root():
    return HTMLResponse('<h1>Hi from FastAPI!</>')

@app.post('/login', tags=['auth'])
async def login(user: User):
    if user.email == "admin@admin.com" and user.password == "admin12345":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)


# response_model=List[Movie] -> indicamos que devolvemos una Lista de tipo Movie
@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer)])
# la func retorna una Lista de tipo Movie
async def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    # retorna un contenido de movies en formato JSON
    return JSONResponse(status_code=200, content=jsonable_encoder(result))  

# http://127.0.0.1:5000/movies/2
@app.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
async def get_movie_by_id(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# http://127.0.0.1:5000/movies/?category=Romantico
@app.get('/movies/', tags=['movies'], response_model=List[Movie])
async def get_movie_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = list(filter(lambda item: item['category'] == category, movies))
    return JSONResponse(content=data)


@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
async def create_movie(movie: Movie):
    # creo una sesion para conectarme a la base de datos
    db = Session()
    new_movie = MovieModel(**movie.dict())
    # añado la movie creada a la db
    db.add(new_movie)
    # guardo el dato en la db
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})
   

# response_model=dict -> la respuesta sera un diccionario
@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
async def update_movie(id: int, movie: Movie) -> dict: # la funcion devolvera un diccionario 
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(status_code=200, content={"message": "The movie has been modified."})


# http://127.0.0.1:5000/movies/2
@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
async def delete_movie(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message": "The movie has been removed."})
