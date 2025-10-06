import os
from dotenv import load_dotenv

load_dotenv()

# Auth0 Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "dev-ioniacov.eu.auth0.com")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "https://api.localhost/receipts")
AUTH0_ISSUER = os.getenv("AUTH0_ISSUER", "https://dev-ioniacov.eu.auth0.com/")
