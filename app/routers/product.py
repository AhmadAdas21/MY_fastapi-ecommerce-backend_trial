from fastapi import APIRouter, HTTPException, Query
from app.schemas.product_schema import ProductCreate, ProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

products = [
    {
        "id": 1,
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 1200,
        "stock_quantity": 10,
        "category_id": 1
    },
    {
        "id": 2,
        "name": "Headphones",
        "description": "Wireless headphones",
        "price": 150,
        "stock_quantity": 25,
        "category_id": 1
    }
]

next_product_id = 3


@router.get("/")
def get_products(
    search: str | None = None,
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0)
):
    result = products

    if search:
        result = [
            product for product in result
            if search.lower() in product["name"].lower()
        ]

    if min_price is not None:
        result = [
            product for product in result
            if product["price"] >= min_price
        ]

    if max_price is not None:
        result = [
            product for product in result
            if product["price"] <= max_price
        ]

    return result


@router.get("/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")


@router.post("/")
def create_product(product: ProductCreate):
    global next_product_id

    new_product = {
        "id": next_product_id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock_quantity": product.stock_quantity,
        "category_id": product.category_id
    }

    products.append(new_product)
    next_product_id += 1

    return {
        "message": "Product created successfully",
        "product": new_product
    }


@router.put("/{product_id}")
def update_product(product_id: int, updated_product: ProductUpdate):
    for product in products:
        if product["id"] == product_id:
            update_data = updated_product.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                product[key] = value

            return {
                "message": "Product updated successfully",
                "product": product
            }

    raise HTTPException(status_code=404, detail="Product not found")


@router.delete("/{product_id}")
def delete_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {
                "message": "Product deleted successfully"
            }

    raise HTTPException(status_code=404, detail="Product not found")