from app.db.connection import get_db


collection = "subjects"

class Subjects():
    
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