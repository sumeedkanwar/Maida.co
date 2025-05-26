# Image Moderation API

A FastAPI-based image moderation API with MongoDB for token and usage tracking, and a simple HTML/JS frontend.

## Prerequisites

- Docker and Docker Compose
- Git

## Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd image-moderation-api
   ```

2. Copy the example environment file:

   ```bash
   cp backend/.env.example backend/.env
   ```

3. Build and run the containers:
   ```bash
   docker-compose up --build
   ```

## Usage

- **Backend**: Accessible at `http://localhost:7000`
  - API documentation: `http://localhost:7000/docs`
  - Endpoints:
    - `POST /auth/tokens`: Create a new token (admin-only)
    - `GET /auth/tokens`: List all tokens (admin-only)
    - `DELETE /auth/tokens/{token}`: Delete a token (admin-only)
    - `POST /moderate`: Moderate an image URL
- **Frontend**: Accessible at `http://localhost`
  - Enter a token and image URL to moderate images.

## Generating a Token

1. Use an admin token (initially create one manually in MongoDB or via a test endpoint).
2. Access `POST /auth/tokens` with the admin token to generate new tokens.

## Git Workflow

- **Main branch**: `main` (production-ready)
- **Pull Requests**: Submit PRs for code review before merging into `main`.

## Notes

- The image moderation logic is a placeholder checking image size/format. Replace with a real moderation service (e.g., AWS Rekognition) in production.
- Ensure MongoDB URI is correctly set in `.env`.
