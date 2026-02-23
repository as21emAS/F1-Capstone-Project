# API Specification

> 🚧 **This document is a work in progress.** It will be completed during Increment 2.
> 
> For interactive API docs, run the backend locally and visit `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc`.

## Overview

The F1 Race Predictor backend exposes a RESTful API built with FastAPI. All endpoints are prefixed with `/api`.

## Endpoints

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Returns system health status and schema integrity check |

### Races
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/races` | List all races |
| GET | `/api/races/{race_id}` | Get a specific race by ID |

### Drivers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/drivers` | List all drivers |
| GET | `/api/drivers/{driver_id}` | Get a specific driver by ID |

### Predictions
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predictions` | Submit race parameters and get a prediction |
| GET | `/api/predictions/{race_id}` | Get prediction results for a specific race |

### Circuits
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/circuits` | List all circuits |
| GET | `/api/circuits/{circuit_id}` | Get a specific circuit by ID |

---

*Full request/response schemas, query parameters, and error codes to be documented in Increment 2.*
