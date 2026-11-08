from pydantic import BaseModel, ConfigDict, Field

class DishIngredientCreate(BaseModel):
    ingredient_id: int = Field(gt=0, description="ID ингредиента", examples=[1, 2, 3])
    dish_id: int = Field(gt=0, description="ID блюда", examples=[1, 2, 3])
    quantity: int = Field(gt=0, description="Количество ингредиента", examples=[100, 200, 300])

class DishIngredientUpdate(BaseModel):
    quantity: int | None = Field(default=None, gt=0, description="Количество ингредиента", examples=[100, 200, 300])

class DishIngredientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    dish_ingredient_id: int
    ingredient_id: int
    dish_id: int
    quantity: int
