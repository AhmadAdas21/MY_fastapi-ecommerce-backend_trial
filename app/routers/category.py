from fastapi import APIRouter, HTTPException
from app.schemas.category_schema import CategoryCreate, CategoryUpdate

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

categories = [
    {
        "id": 1,
        "name": "Electronics",
        "description": "Electronic devices and accessories"
    },
    {
        "id": 2,
        "name": "Clothes",
        "description": "Clothing products"
    }
]

next_category_id = 3


@router.get("/")
def get_categories():
    return categories


@router.get("/{category_id}")
def get_category(category_id: int):
    for category in categories:
        if category["id"] == category_id:
            return category

    raise HTTPException(status_code=404, detail="Category not found")


@router.post("/")
def create_category(category: CategoryCreate):
    global next_category_id

    new_category = {
        "id": next_category_id,
        "name": category.name,
        "description": category.description
    }

    categories.append(new_category)
    next_category_id += 1

    return {
        "message": "Category created successfully",
        "category": new_category
    }


@router.put("/{category_id}")
def update_category(category_id: int, updated_category: CategoryUpdate):
    for category in categories:
        if category["id"] == category_id:
            update_data = updated_category.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                category[key] = value

            return {
                "message": "Category updated successfully",
                "category": category
            }

    raise HTTPException(status_code=404, detail="Category not found")


@router.delete("/{category_id}")
def delete_category(category_id: int):
    for category in categories:
        if category["id"] == category_id:
            categories.remove(category)
            return {
                "message": "Category deleted successfully"
            }

    raise HTTPException(status_code=404, detail="Category not found")