from pydantic import BaseModel, Field

class CartItemCreate(BaseModel):

    ##user_id: int
    product_id: int
    quantity:int =Field(..., gt=0)



class CartItemUpdate(BaseModel):
    
    quantity: int = Field(..., gt=0)