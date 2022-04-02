from bson import ObjectId

from app.db.connection import get_db


collection = "files"


class Files:
    @staticmethod
    async def insert_files(input_data: dict):
        db = await get_db()
        if ("msgs" in input_data.keys()) or ("photos" in input_data.keys()):
            db_input_data = []
            if "msgs" in input_data.keys():
                input_msgs = [{"subject_id": input_data["subject_id"], "message_text": text} for text in input_data["msgs"]]
                db_input_data += input_msgs
            if "photos" in input_data.keys():
                input_photos_set = set(input_data["photos"])
                input_photos = [{"subject_id": input_data["subject_id"], "photo_id": id} for id in input_photos_set]
                db_input_data += input_photos
            await db[collection].insert_many(db_input_data)
        
    @staticmethod
    async def get_files(subject_id: ObjectId):
        db = await get_db()
        files = db[collection].find({"subject_id": subject_id})
        files = await files.to_list(length=None)
        return files