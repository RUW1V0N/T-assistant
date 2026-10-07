import asyncio

from sqlalchemy import select

from app.db.database import async_session
from app.models.exercise import Exercise
from src.seed_data.exercises import EXERCISES


async def seed_exercises():
    async with async_session() as session:
        result = await session.execute(
            select(Exercise.name)
        )

        existing_names = set(result.scalars().all())

        new_exercises = [
            Exercise(**exercise_data)
            for exercise_data in EXERCISES
            if exercise_data["name"] not in existing_names
        ]
        
        if not new_exercises: 
            print("No new exercises to add")
            return

        session.add_all(new_exercises)

        await session.commit()

        print(f"Added {len(new_exercises)} exercises.")


if __name__ == "__main__":
    asyncio.run(seed_exercises())