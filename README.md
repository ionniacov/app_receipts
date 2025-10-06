# Receipts App with Auth0 Integration

A full-stack application with a Python FastAPI backend and a simple frontend that demonstrates Auth0 authentication with PKCE (Proof Key for Code Exchange) flow.

## Features

- **Backend**: FastAPI REST API with JWT token validation
- **Frontend**: Simple HTML/JavaScript client with Auth0 SPA SDK
- **Authentication**: Auth0 with PKCE authorization code flow
- **Security**: CORS enabled, JWT validation with JWKS
- **Data**: Static in-memory data filtered by user

## Project Structure

```
app_chitante/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html           # Frontend application
│   └── styles.css           # Styling
├── frontend_server.py       # Frontend server
├── start_backend.py         # Backend startup script
├── start_frontend.py        # Frontend startup script
└── README.md               # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r backend/requirements.txt
```

### 2. Auth0 Configuration

1. Create an Auth0 account at [auth0.com](https://auth0.com)
2. Create a new Single Page Application (SPA)
3. Configure the following settings:
   - **Allowed Callback URLs**: `http://localhost:8001`
   - **Allowed Logout URLs**: `http://localhost:8001`
   - **Allowed Web Origins**: `http://localhost:8001`
   - **Allowed Origins (CORS)**: `http://localhost:8001`

4. Create an API in Auth0:
   - **Identifier**: `https://api.localhost/receipts`
   - **Signing Algorithm**: RS256

5. Update the Auth0 configuration in `backend/config.py`:
   ```python
   AUTH0_DOMAIN = "your-domain.auth0.com"
   AUTH0_AUDIENCE = "https://api.localhost/receipts"
   AUTH0_ISSUER = "https://your-domain.auth0.com/"
   ```

6. Update the frontend configuration in `frontend/index.html`:
   ```javascript
   domain: "your-domain.auth0.com",
   clientId: "your-client-id",
   ```

### 3. Run the Application

#### Option 1: Using the startup scripts

```bash
# Terminal 1 - Start backend
python start_backend.py

# Terminal 2 - Start frontend
python start_frontend.py
```

#### Option 2: Manual startup

```bash
# Terminal 1 - Start backend
#cd backend
#uvicorn main:app --host 127.0.0.1 --port 8000 --reload
python start_backend.py

# Terminal 2 - Start frontend
#python frontend_server.py
python start_frontend.py
```

### 4. Access the Application

- **Frontend**: http://localhost:8001
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## How It Works

### Authentication Flow

1. User clicks "Login" button
2. Frontend redirects to Auth0 with PKCE parameters
3. User authenticates with Auth0
4. Auth0 redirects back with authorization code
5. Frontend exchanges code for access token (PKCE flow)
6. Access token is used to authenticate API requests

### API Endpoints

- `GET /receipts` - Get all receipts for the authenticated user
- `GET /receipts/{receipt_code}` - Get a specific receipt (if owned by user)

### Security Features

- **JWT Validation**: Tokens are validated using Auth0's JWKS
- **CORS**: Configured for frontend-backend communication
- **User Isolation**: Users can only access their own receipts
- **PKCE**: Secure authorization code flow for SPAs

## Testing

1. Open http://localhost:8001
2. Click "Login" to authenticate with Auth0
3. After successful login, click "My Receipts" to fetch data
4. The API will return receipts filtered by your user ID

## Sample Data

The application includes sample receipts with different owners:
- `auth0|68dfb748e1faeb183927781e` - 2 receipts
- `auth0|userB` - 1 receipt

## Troubleshooting

### Common Issues

1. **CORS errors**: Ensure the frontend URL is in the CORS allowed origins
2. **Token validation errors**: Check Auth0 configuration and audience
3. **Login redirect issues**: Verify callback URLs in Auth0 dashboard
4. **No receipts returned**: Check if your user ID matches the sample data

### Debug Mode

Enable debug logging by setting the log level to "debug" in the startup scripts.

## Dependencies

### Backend
- FastAPI
- python-jose (JWT handling)
- requests (JWKS fetching)
- python-dotenv (environment variables)

### Frontend
- Auth0 SPA SDK (CDN)
- Vanilla JavaScript

## Security Notes

- This is a demo application with in-memory data
- In production, use a proper database
- Store sensitive configuration in environment variables
- Implement proper error handling and logging
- Consider rate limiting and additional security measures
