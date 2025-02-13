from fastapi import FastAPI, Query, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from products import ProductAPIClient
import uvicorn
import jwt
import datetime
import logging

SECRET_KEY = "imagemkaersecretkey"
ALGORITHM = "HS256"
app = FastAPI()
client = ProductAPIClient()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")



@app.post("/auth/")
def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "admin" or form_data.password != "imagemaker":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    token = jwt.encode({"sub": form_data.username, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return {"access_token": token, "token_type": "bearer"}

@app.get("/products")
def get_products(min_price: float = Query(None, description="Minimum price"), max_price: float = Query(None, description="Maximum price"),user: str = Depends(get_current_user)):
    try:
        min_price = min_price if min_price is not None else 0
        max_price = max_price if max_price is not None else float('inf')
        products = client.get_all_products(min_price, max_price)
    except Exception as e:
        logging.error(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving products")
    return {"products": products}

@app.get("/products/products_id")
def get_product(product_id: int, user: str = Depends(get_current_user)):
    try:
        product = client.get_product_by_id(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching product: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving product")


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)


