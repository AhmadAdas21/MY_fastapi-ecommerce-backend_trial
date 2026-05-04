from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.dependencies import get_current_admin
from app.database import get_db
from app.models.category_model import Category
from app.schemas.category_schema import CategoryCreate, CategoryUpdate

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories


@router.get("/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


@router.post("/")
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return {
        "message": "Category created successfully",
        "category": new_category
    }


@router.put("/{category_id}")
def update_category(
    category_id: int,
    updated_category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    update_data = updated_category.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return {
        "message": "Category updated successfully",
        "category": category
    }


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()

    return {
        "message": "Category deleted successfully"
    }