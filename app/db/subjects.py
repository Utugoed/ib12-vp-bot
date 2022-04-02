from app.db.connection import get_db


collection = "subjects"


class Subjects:
    @staticmethod
    async def insert_subject(sbj_name: str):
        db = await get_db()
        db[collection].insert_one({"name": sbj_name.upper()})

    @staticmethod
    async def get_subjects():
        db = await get_db()
        result = db[collection].find()
        sbj_list = [subject async for subject in result]
        return sbj_list

    @staticmethod
    async def get_subject_id(name: str):
        db = await get_db()
        result = await db[collection].find_one({"name": name.upper()})
        if result is not None:
            id = result["_id"]
            return id

    @staticmethod
    async def delete_subject(name: str):
        db = await get_db()
        result = await db[collection].delete_one({"name": name.upper()})
