# OpenRouter AI - FastAPI Application

## Overview
This project is a **FastAPI-based reverse proxy** for OpenRouter, designed for **efficient AI model request handling** with features such as **request caching, streaming responses, and authentication**.

## Features
- **FastAPI-based API** for handling OpenRouter requests.
- **Caching mechanism** to optimize repeated queries.
- **CORS middleware** for secure cross-origin requests.
- **Streaming response handling** for AI-generated completions.
- **Authentication and request validation**.
- **Deployment using systemd on Ubuntu**.

---

## Installation & Setup

### Prerequisites
- Ubuntu 20.04+  
- Python 3.8+  
- FastAPI, Uvicorn  
- Systemd for service management  

### 1. Clone the Repository
```sh
git clone https://github.com/Luxman-Madapatha/openrouter.git
cd openrouter
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
```
Add to your .env file
OPENROUTER_API_KEY = "key"
API_VALIDATION_TOKEN = "key"
```

### 4. Create a Systemd Service File
Create a new systemd service file:
```sh
sudo nano /etc/systemd/system/openrouter.service
```

Paste the following:
```ini
[Unit]
Description=OpenRouter AI
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=on-failure
RestartSec=5
User=anvil
WorkingDirectory=/home/anvil/openRouter
ExecStart=uvicorn app:app --host 0.0.0.0 --port 8888 --reload

[Install]
WantedBy=multi-user.target
```

### 5. Enable and Start the Service
```sh
sudo systemctl daemon-reload
sudo systemctl enable openrouter
sudo systemctl start openrouter
```

### 6. Check Service Status
```sh
sudo systemctl status openrouter
```

### 7. Restart or Stop Service
```sh
sudo systemctl restart openrouter
sudo systemctl stop openrouter
```

## API Endpoints

### Root Endpoint
```http
GET /
```
Returns a basic HTML response.


## License
This project is licensed under **MIT License**.

## Author
Developed by **Luxman Madapatha**.
