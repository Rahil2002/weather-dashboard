# Weather Dashboard API

A live weather API built with Python Flask that returns real-time weather 
data for any city using the OpenWeatherMap API.

## Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | API info and usage |
| `GET /weather?city=London` | Live weather for any city |
| `GET /health` | Health check |

## Tech Stack
Python · Flask · Docker · Jenkins · Azure

## How to run locally

```bash
pip install -r requirements.txt
python app.py
```