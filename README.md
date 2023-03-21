# Intro FastAPI

![](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

## Instalacion

### Python3

Se necesita al menos _Python v3.7_ o superior para correr adecuadamente la app.

```bash
sudo apt install python3 python3-pip python3-venv
```

### Virtual Environment (Activar)

```bash
python3 -m venv .venv-app
source .venv-app/bin/activate
```

### Instalar librerias

1. A través de requirements.txt 

`pip3 install -r requirements.txt`

### Run app

`uvicorn main:app --reload`