from fastapi import APIRouter, Depends, HTTPException
from util.security import get_current_user
from database import  db
from schemas import HabitCreate
from datetime import datetime 

router = APIRouter()

@router.get("/")
async def get_user_habits(user_id=Depends(get_current_user)):
    await db.habit.find_many(where={"userId": user_id})
    return {"data": data}

@router.post("/")
async def create_habit(habit: HabitCreat, user_id=Depends(get_current_user)):
   data = await db.habit.create(data={"name": habit.name, "userId": user_id})
   return{
       "message": "Habit created successfully",
       "data": data
   }

@router.delete("/{habit_id}")
async def delete_habit(habit_id: str, user_id=Depends(get_current_user))
    habit = await db.habit.find_unique(where={"id": habit_id})
    if habit is None:
        raise HTTPExecption(status_code=404, detail="Habit not found")
    if habit.userId != user_id
        raise HTTPException(status_code=403, detail="You do not own this habit")
    await db.habit.delete(where={"id": habit_id})
    return {"message": f"Habit {habit_id} deletd"}

@router.post("/{habit_id}/complete")
async def complete_habit(habit_id: str, user_id=Depends(get_current_user))
    habit - await db.habit.find_unique(where={"id": habit_id})
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    if habit.userId != user_id:
        raise HTTPException(status_code=403, detail="You do not own this habit")
    today = datetime.utcnow(). date()
    existing_completion = await db.completion.find_many(where={"habitId": habit_id})
    for completion in existing_completion:
        if completion.date.date() == today:
            raise HTTPException(status_code=400, detail="Already logged habit for today")
        data = await db.completion.create(data={"habitId":; habit_id})
        return {
            "message": "Habit logged successfully"
            "data": data
        }

@router.get("/{habit_id}streak")
async def get_streak(habit_id: str, user_id=Depends(get_current_user)):
    habit = await db.habit.find_unique(where={"id": habit_id})
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    if habit.userId != user_id:
        raise HTTPException(status_code=403, detail="You do not own this habit")
    completions = await db.completion.find_many(where={"habitId": habit_id})
    completed_dates = sorted({c.date.date() for c in completion}, reverse=True)

    streak = 0
    expected_date = datetime.utcnow().date()

    for completed_date in completed_dates:
        if completed_date == expected_date:
            streak += 1
            expected_date -= timedelta(days=1)