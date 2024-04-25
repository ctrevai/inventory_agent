from fastapi import FastAPI
import random
import json
import os
import csv
from fastapi import HTTPException
from mangum import Mangum
from pydantic import BaseModel
from uuid import uuid4
from typing import Optional
from fastapi.encoders import jsonable_encoder


# create api root entry with FastAPI
app = FastAPI()
handler = Mangum(app)
# product model


class Product(BaseModel):
    name: str
    color: str
    price: float
    quantity: int
    manuf: str
    product_id: Optional[str] = uuid4().hex


PRODUCT_FILE = "product.json"
PRODUCT_DB = []

if os.path.exists(PRODUCT_FILE):
    with open(PRODUCT_FILE, "r") as f:
        PRODUCT_DB = json.load(f)
else:
    # open csv file and dumb to json
    with open("../../Data/productlist.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            new_product = Product(
                name=row[1],
                color=row[2],
                price=float(row[3]),
                quantity=int(row[4]),
                manuf=row[5],
                product_id=uuid4().hex
            )
            json_product = jsonable_encoder(new_product)
            PRODUCT_DB.append(json_product)

    with open(PRODUCT_FILE, "w") as f:
        json.dump(PRODUCT_DB, f)
# /


@app.get("/")
async def root():
    return {"message": "Welcome to Inventory API"}

# /list-products


@app.get("/list-products")
async def list_products():
    return {"products": PRODUCT_DB}

# /product-by-index


@app.get("/product-by-index")
async def product_by_index(index: int):
    if index < 0 or index >= len(PRODUCT_DB):
        raise HTTPException(status_code=404, detail=f"Product not found: Index {
                            index} is out of range.")
    return {"product": PRODUCT_DB[index]}

# /get-random-product


@app.get("/get-random-product")
async def get_random_product():
    return {"product": random.choice(PRODUCT_DB)}

# /add-product


@app.post("/add-product")
async def add_product(product: Product):
    product.product_id = uuid4().hex
    json_product = jsonable_encoder(product)
    PRODUCT_DB.append(json_product)
    with open(PRODUCT_FILE, "w") as f:
        json.dump(PRODUCT_DB, f)
    return {"message": f"Product {product} added to product list successfully", "product_id": product.product_id}

# /get-product?id={id}


@app.get("/get-product")
async def get_product(product_id: str):
    for product in PRODUCT_DB:
        if product["product_id"] == product_id:
            return {"product": product}
    raise HTTPException(
        status_code=404, detail=f"Product not found: {product_id}")
