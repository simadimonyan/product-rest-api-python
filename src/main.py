from typing import Optional
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from database import Database
from models.product import ProductResponse

app = FastAPI(
    title="Products API",
    version="1",
    contact={
        "name": "Dimitri Simonyan",
        "email": "simadimonyan@gmail.com",
        "url": " https://github.com/simadimonyan"
    }
)
db = Database()

@app.get("/api/products/product/{id}", tags=["v1"])
def getProduct(id: str):
    product = db.getProduct(id)
    if (product != None):
        return JSONResponse(content=[product.toJSON()])
    else:
        return JSONResponse(content={"message": "The product does not exist", "product": "null"})

@app.get("/api/products/", tags=["v1"])
def getAllProducts(
    category: Optional[str] = Query(None, description="Filter by product category"),
    name: Optional[str] = Query(None, description="Filter by product name"),
    max_price: Optional[float] = Query(None, description="Filter by maximum price"),
    min_price: Optional[float] = Query(None, description="Filter by minimum price"),
    amount: Optional[int] = Query(None, description="Filter by product amount"),
    currency: Optional[str] = Query(None, description="Filter by product currency")
):
    products = db.getAllProducts(category, name, max_price, min_price, amount, currency)  
    response = []

    for p in products:
        response.append(p.toJSON())

    return JSONResponse(content=response)

@app.post("/api/products/product/", response_model=ProductResponse, tags=["v1"])
def postProduct(product: ProductResponse):
    try:
        result = db.addProduct(product.category, product.name, product.amount, product.cost, product.currency)
        return JSONResponse(content={"message": "The product created successfully", "product": result.toJSON()})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": f"Error ocurred: {e}", "product": "null"})
    
@app.post("/api/products/products/", response_model=list[ProductResponse], tags=["v1"])
def postProducts(products: list[ProductResponse]):
    try:
        message = "Products created successfully"
        warnings = "Products created but some of them already exist"
        fatal = "All products exist"

        added = []
        errors = 0
        (added, errors) = db.addProducts(products)
        
        if (errors == len(added)):
            message = fatal
        elif (errors > 0):
            message = warnings

        return JSONResponse(content={"message": f"{message}", "products": added})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": f"Error ocurred: {e}", "product": "null"})
    
@app.delete("/api/products/products/", tags=["v1"])
def deleteProducts(ids: list[str] = Query(...)):
    try:
        message = "Products deleted successfully"
        warnings = "Products deleted but some of them do not exist"
        fatal = "All products do not exist"

        deleted = []
        errors = 0
        (deleted, errors) = db.deleteProducts(ids)
        
        if (errors == len(deleted)):
            message = fatal
        elif (errors > 0):
            message = warnings

        return JSONResponse(content={"message": f"{message}", "products": deleted})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": f"Error ocurred: {e}", "product": "null"})
            
@app.delete("/api/products/product/{id}", tags=["v1"])
def deleteProduct(id: str):
    try:
        product = db.deleteProduct(id)
        return JSONResponse(content={"message": "The product deleted successfully", "product": product.toJSON()})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": f"The product already deleted", "product": "null"})

@app.put("/api/products/product/{id}", response_model=ProductResponse, tags=["v1"])
def putProduct(id: str, product: ProductResponse):
    try:
        result = db.updateProduct(id, product.category, product.name, product.amount, product.cost, product.currency)
        return JSONResponse(content={"message": "The product updated successfully", "product": result.toJSON()})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": f"The product does not exist", "product": "null"})