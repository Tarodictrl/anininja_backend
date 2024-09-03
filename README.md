<h1 align="center">AniNinja</h1>
<p align="center"><i>Website for watching anime for free.</i></p>
<div align="center">
<img src="https://img.shields.io/badge/Python-3.11-brightgreen.svg">
</br>
<img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi">
<img src="https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D">
<img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white">
</div>

## 📝 Description

API url: https://api.anininja.ru
<br>
Redoc url: https://api.anininja.ru/docs

## 🛠️ Preparation

### Create .env file

In the root folder of the project, you need to create `.env` file such as [sample.env](https://github.com/Tarodictrl/anininja_backend/blob/develop/sample.env)
### Install poetry

#### Using pip:

`pip install poetry`
or
`pip3 install poetry`

#### Using pipx:

`pipx install poetry`

#### Using curl

`curl -sSL https://install.python-poetry.org | python3 -`

### Install dependencies

`poetry install`


## 🏹 Run

### With poetry

`poetry run uvicorn app.main:app --reload`

### With poetry shell

`poetry shell`

`uvicorn app.main:app --reload`

### With docker

`docker compose up --build -d`
