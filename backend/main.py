import requests
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt, JWTError
from jose.backends import RSAKey
from config import AUTH0_DOMAIN, AUTH0_AUDIENCE, AUTH0_ISSUER

JWKS_URL = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
ALGORITHMS = ["RS256"]

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory "database"
RECEIPTS = {
    "rct_1": {"id": 1, "amount": 120.5, "currency": "RON", "owner": "auth0|68dfb748e1faeb183927781e"},
    "rct_2": {"id": 2, "amount": 59.9,  "currency": "RON", "owner": "auth0|userB"},
    "rct_3": {"id": 3, "amount": 999.0, "currency": "RON", "owner": "auth0|68dfb748e1faeb183927781e"},
}

_jwks_cache = None

def get_jwks():
    """Download and cache JWKS (JSON Web Key Set) from Auth0"""
    global _jwks_cache
    if _jwks_cache is None:
        resp = requests.get(JWKS_URL)
        resp.raise_for_status()
        _jwks_cache = resp.json()
    return _jwks_cache

def get_current_user(request: Request):
    """Extract and validate JWT from Authorization header"""
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth.split(" ")[1]

    # 1. Get JWT header (contains the key id - kid)
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid")

    # 2. Find the public key that matches kid
    jwks = get_jwks()
    key = None
    for jwk in jwks["keys"]:
        if jwk["kid"] == kid:
            key = jwk
            break
    if not key:
        raise HTTPException(status_code=401, detail="Invalid key ID")

    # 3. Convert JWK to RSA key
    try:
        rsa_key = RSAKey(key, algorithm="RS256")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid key format: {str(e)}")

    # 4. Validate signature and claims
    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=AUTH0_AUDIENCE,
            issuer=AUTH0_ISSUER
        )
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token invalid: {str(e)}")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return user_id

@app.get("/receipts")
def list_receipts(current_user: str = Depends(get_current_user)):
    """Return receipts belonging to the current user"""
    filtered = [r for r in RECEIPTS.values() if r["owner"] == current_user]
    return {"user": current_user, "receipts": filtered}

@app.get("/receipts/{receipt_code}")
def get_receipt(receipt_code: str, current_user: str = Depends(get_current_user)):
    """Return a single receipt if it belongs to the current user"""
    r = RECEIPTS.get(receipt_code)
    if not r:
        raise HTTPException(status_code=404, detail="Receipt not found")
    if r["owner"] != current_user:
        raise HTTPException(status_code=403, detail="Not allowed")
    return r
