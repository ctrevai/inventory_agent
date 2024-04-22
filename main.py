from fastapi import FastAPI
import random

# create api root entry with FastAPI
app = FastAPI()

PRODUCT_DB = ["shaver", "egg", "cola"]

# /


@app.get("/")
def root():
    return {"message": "Welcome to Inventory API"}

# /list-products


@app.get("/list-products")
def list_products():
    return {"products": PRODUCT_DB}

# /product-by-index


@app.get("/product-by-index")
def product_by_index(index):
    return {"product": PRODUCT_DB[index]}

# /get-random-product


@app.get("/get-random-product")
def get_random_product():
    return {"product": random.choice(PRODUCT_DB)}

# /add-product


@app.post("/add-product")
def add_product(product):
    return {"message": "Add product"}

# /get-product?id={id}


app.get("/get-product")


def get_product(id):
    return {"product": PRODUCT_DB[id]}