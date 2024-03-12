from fastapi import FastAPI, HTTPException
from typing import List, Dict
from database import MongoDb
from pydantic import BaseModel

app = FastAPI()
db = MongoDb()


class LightSetup(BaseModel):
    light_brightness_list: List[int]
    expected_brightness: int


def find_solutions(lights: List[int], expect: int):
    result = []
    lights.sort()

    def find_solution(start=0, path=[], total=0):
        if total == expect:
            result.append(path.copy())
            return
        if total > expect:
            return

        for i in range(start, len(lights)):
            if i > start and lights[i] == lights[i - 1]:
                continue
            path.append(lights[i])
            find_solution(i, path, total + lights[i])
            path.pop()

    find_solution()
    return result


@app.post("/calculate-lights/")
def calculate_lights(request: LightSetup):
    if request.expected_brightness <= 0:
        return {"message": "No solution found", "solutions": []}
    solutions = find_solutions(request.light_brightness_list, request.expected_brightness)
    if not solutions:
        return {"message": "No solution found", "solutions": []}

    return {"message": "Solutions found", "solutions": solutions}


@app.get("/rooms/{room_id}/lights")
async def get_lights(room_id: int):
    room = await db.get_room(room_id=room_id)
    if not room:
        return {"error": "Room not found"}

    lights_in_room = await db.get_lights_in_room(room_id=room_id)
    return {"lights": lights_in_room}
