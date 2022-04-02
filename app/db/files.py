from app.db.connection import get_db


collection = "files"


class Files:
    @staticmethod
    async def insert_files(input_data: dict):
        db = await get_db()
        input_data = [{"subject": input_data["subject_id"], "message_id": id} for id in input_data["files"]]
        db[collection].insert(input_data)