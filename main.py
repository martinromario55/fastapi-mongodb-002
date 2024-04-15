from fastapi import FastAPI, APIRouter, HTTPException, status

from config import collection
from database.schemas import all_tasks
from database.models import Todo

from bson.objectid import ObjectId
from datetime import datetime


app = FastAPI()
router = APIRouter()

@router.get("/")
async def get_all_todos():
    data = collection.find({"is_deleted": False}) # Return items that have not been deleted
    return all_tasks(data)


@router.post("/")
async def create_todo(todo: Todo):
    try:
        resp = collection.insert_one(dict(todo))
        return {"id": str(resp.inserted_id), "status": status.HTTP_201_CREATED}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
@router.put("/{id}")
async def update_todo(id: str, updated_todo: Todo):
    try:
        # Check if task exists
        existing_task = collection.find_one({"_id": ObjectId(id), "is_deleted": False})
        
        if not existing_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
        # Update updated time
        updated_todo.updated_at = int(datetime.timestamp(datetime.now()))
        
        collection.update_one({"_id": ObjectId(id)}, {"$set": dict(updated_todo)})
        
        return {"status": status.HTTP_200_OK, "message": "Task updated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
@router.delete("/{id}")
async def delete_todo(id: str):
    try:
        # Check if task exists
        existing_task = collection.find_one({"_id": ObjectId(id), "is_deleted": False})
        
        if not existing_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
        collection.update_one({"_id": ObjectId(id)}, {"$set": {"is_deleted": True}})
        
        return {"status": status.HTTP_200_OK, "message": "Task deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

app.include_router(router)