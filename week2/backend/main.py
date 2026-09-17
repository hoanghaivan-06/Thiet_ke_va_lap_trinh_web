from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI()

#====== Static Files =====

app.mount("/static", StaticFiles(directory = "../frontend"), name = "static")
# ===================
# Model 1
# ===================
#class Item(BaseModel):
#    id: int
#    name: str
#    price: float

# Data sent by client when creating/updating an item
class ItemCreate(BaseModel):
    name: str
    price: float
# Data sent by client when partially updating an item
class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
# Data returned to client
class ItemPublic(BaseModel): # LAB 2
    id: int
    name:str
    price: float

# Response model for GET /items
class ItemListResponse(BaseModel):
    items: list[ItemPublic]
    total: int
    skip: int
    limit: int
# Request model for prediction
class HousePriceRequest(BaseModel):
    area_sqm: float = Field(gt=0)
    bedrooms: int = Field(ge=0)
    distance_to_center_km: float
# Response model for prediction
class HousePricePrediction(BaseModel):
    predicted_price: float
    currency: str = "VND"

# ===============
# In-memory data
# ===============
# items: list[Item] = []      ==LAB1==
items: list[ItemPublic] = [] # Lab2
next_id = 1

# ===============
# Root
# ===============

@app.get("/")
def read_root():
    return {"Message":"Hello World"}

# ================
# Get /items
# Filtering + Sorting + Pagination + Envelope
# Get all items (Lab1)
# With pagination ( lab 2)
# ================


# @app.get("/items")   === Lab1===
# def get_items():
#    return items

@app.get("/items", response_model=ItemListResponse)
def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),

    min_price: float | None = None,
    max_price: float | None = None,

    q: str | None = Query(None, min_length=2),

    sort_by: str = Query(
        "id",
        pattern="^(id|name|price)$"
    ),

    order: str = Query(
        "asc",
        pattern="^(asc|desc)$"
    )
):

    # Start with all item
    filtered_items = items.copy()

    # Filter by minimum price
    if min_price is not None:
        filtered_items = [
            item
            for item in filtered_items
            if item.price >= min_price
        ]
    # Filter by maximum price
    if max_price is not None:
        filtered_items = [
            item
            for item in filtered_items
            if item.price <= max_price
        ]
    # Search by name (case insentive substring search)
    if q is not None:
        filtered_items = [
            item
            for item in filtered_items
            if q.lower() in item.name.lower()
        ]
    # Sort
    filtered_items.sort(
        key=lambda item: getattr(item, sort_by),
        reverse=(order == "desc")
    )
    # Total before pagination
    total = len(filtered_items)
    # pagination after filtering + sorting
    paginated_items = filtered_items[
        skip:skip + limit
    ]
    # return envelope
    return {
        "items": paginated_items,
        "total": total,
        "skip": skip,
        "limit": limit
    }

# ================
# GET /items/{item_id}
# GET one item
# ================

"""@app.get("/items/{item_id}") /lab1/
def get_item(item_id:int):
    for item in items:
        if item.id == item_id:
            return item

    raise HTTPException(
        status_code = 404,
        detail = "Item not found"
    )"""

@app.get("/items/{item_id}", response_model=ItemPublic)
def get_item(item_id: int):

    for item in items:
        if item.id == item_id:
            return item

    raise HTTPException(
        status_code=404,
        detail="Item not found"
    )


# ===================
# POST /items
# Cretae items
# ===================

""" @app.post("/items", status_code = 201)  /Lab1/
def create_item(data: ItemCreate):
    global next_id
    item = Item(
        id = next_id,
        name=  data.name,
        price = data.price
    )

    items.append(item)
    next_id += 1
    return item """ 

@app.post(
    "/items",
    response_model=ItemPublic,
    status_code=201
)
def create_item(data: ItemCreate):

    global next_id

    # Check duplicate

    for item in items:

        if item.name.lower() == data.name.lower():

            raise HTTPException(
                status_code=409,
                detail="Item with this name already exists"
            )

    # Create item
    item = ItemPublic(
        id=next_id,
        name=data.name,
        price=data.price
    )

    items.append(item)

    next_id += 1

    return item


# ===============
# PUT /items/{item_id}
# Update item
# ===============

"""@app.put("/items/{item_id}")
def update_item(item_id: int, data: ItemCreate):
    for i, item in enumerate(items):
        if item.id == item_id:
            updated_item = Item(
                id = item_id,
                name = data.name,
                price=  data.price
            )

            items[i] = updated_item
            return updated_item

    raise HTTPException(
        status_code = 404,
        detail = "Item not found"
    )
"""
@app.put(
    "/items/{item_id}",
    response_model=ItemPublic
)
def update_item(item_id: int, data: ItemCreate):

    for i, item in enumerate(items):

        if item.id == item_id:

            # Check duplicate

            if data.name.lower() != item.name.lower():

                for other_item in items:

                    if (
                        other_item.id != item_id
                        and other_item.name.lower()
                        == data.name.lower()
                    ):

                        raise HTTPException(
                            status_code=409,
                            detail="Item with this name already exists"
                        )

            # replace item
            updated_item = ItemPublic(
                id=item_id,
                name=data.name,
                price=data.price
            )

            items[i] = updated_item

            return updated_item


    raise HTTPException(
        status_code=404,
        detail="Item not found"
    )

# ====================
# Patch /items/{item_id}
# Partial update
# ====================

@app.patch(
    "/items/{item_id}",
    response_model=ItemPublic
)
def patch_item(
    item_id: int,
    data: ItemUpdate
):
    # Find item
    for i, item in enumerate(items):

        if item.id == item_id:

            # Get only fields explicity sent by client 
            updates = data.model_dump(
                exclude_unset=True
            )

            # Check duplicate 
            if "name" in updates:

                new_name = updates["name"]

                if (
                    new_name is not None
                    and new_name.lower() != item.name.lower()
                ):

                    for other_item in items:

                        if (
                            other_item.id != item_id
                            and other_item.name.lower()
                            == new_name.lower()
                        ):

                            raise HTTPException(
                                status_code=409,
                                detail="Item with this name already exists"
                            )
            # update only provided fields
            updated_data = {
                "name": item.name,
                "price": item.price
            }

            if "name" in updates and updates["name"] is not None:
                updated_data["name"] = updates["name"]

            if "price" in updates and updates["price"] is not None:
                updated_data["price"] = updates["price"]

            # Create update

            updated_item = ItemPublic(
                id=item.id,
                name=updated_data["name"],
                price=updated_data["price"]
            )

            items[i] = updated_item

            return updated_item


    raise HTTPException(
        status_code=404,
        detail="Item not found"
    )
# ===============
# DELETE /items/{item_id}
# Delete item
# ===============
"""
@app.delete("/items/{item_id}",status_code = 204)
def delete_item(item_id: int):
    for i, item in enumerate(items):
        if item.id == item_id:
            items.pop(i)

            return
    raise HTTPException(
        status_code= 404,
        detail = "Item not found"
    )
"""
@app.delete(
    "/items/{item_id}",
    status_code=204
)
def delete_item(item_id: int):

    for i, item in enumerate(items):

        if item.id == item_id:

            items.pop(i)
            return

    raise HTTPException(
        status_code=404,
        detail="Item not found"
    )

# ==========================================================
# PART E
# Toy House Price Prediction
# ==========================================================

@app.post(
    "/predict/house-price",
    response_model=HousePricePrediction
)
def predict_house_price(data: HousePriceRequest):

    price = (
        data.area_sqm * 15_000_000
        - data.distance_to_center_km * 5_000_000
        + data.bedrooms * 20_000_000
    )

    return {
        "predicted_price": price,
        "currency": "VND"
    }
