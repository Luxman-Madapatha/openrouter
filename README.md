# OpenRouter FastAPI Application

## Overview
This project is a **FastAPI-based reverse proxy** for OpenRouter, designed to handle AI model requests efficiently. It provides API endpoints for **chat completions**, **model retrieval**, and **request caching**. Its based on the article https://huggingface.co/blog/lynn-mikami/llm-free

## Features
- **FastAPI-based API** for handling OpenRouter requests.
- **Caching mechanism** to optimize repeated queries.
- **CORS middleware** for secure cross-origin requests.
- **Streaming response handling** for AI-generated completions.
- **Authentication and request validation**.

## Installation

### Prerequisites
- Python 3.8+
- FastAPI
- HTTPX
- AnyIO

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/Luxman-Madapatha/openrouter.git
   cd openrouter


