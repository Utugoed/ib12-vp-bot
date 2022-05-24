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
                
                input_msgs_set = set(input_data["msgs"])
                denied_set = set()
                for message in input_msgs_set:
                    file = await db[collection].find_one({"message_text": message})
                    if file is not None:
                        denied_set.add(message)
                input_msgs_set -= denied_set
                
                input_msgs = [
                    {"subject_id": input_data["subject_id"], "message_text": text}
                    for text in input_msgs_set
                ]
                db_input_data += input_msgs
            
            if "photos" in input_data.keys():
                input_photos_list = [
                    {
                    "photo_id": photo[0],
                    "unique_id": photo[1]
                    }
                    for photo in input_data["photos"]]
                
                unique_ids = [photo["unique_id"] for photo in input_photos_list]
                unique_ids_set = set(unique_ids)
                
                denied_set = set()
                for id in unique_ids_set:
                    file = await db[collection].find_one({"unique_id": id})
                    if file is not None:
                        denied_set.add(id)
                
                unique_ids_set -= denied_set
                updated_input_list = []
                
                for photo in input_photos_list:
                    if photo["unique_id"] in unique_ids_set:
                        unique_ids_set -= {photo["unique_id"]}
                        updated_input_list.append(photo)
                
                for photo in updated_input_list:
                    photo["subject_id"] = input_data["subject_id"]
                
                db_input_data += updated_input_list
            if len(db_input_data) != 0:
                await db[collection].insert_many(db_input_data)

    @staticmethod
    async def get_files(subject_id: ObjectId):
        db = await get_db()
        files = db[collection].find({"subject_id": subject_id})
        files = await files.to_list(length=None)
        return files

    @staticmethod
    async def delete_files(input_data: dict):
        db = await get_db()
        if ("msgs" in input_data.keys()) or ("photos" in input_data.keys()):
            db_input_data = []
            if "msgs" in input_data.keys():
                input_msgs = [
                    {"subject_id": input_data["subject_id"], "message_text": text}
                    for text in input_data["msgs"]
                ]
                db_input_data += input_msgs
            if "photos" in input_data.keys():
                input_photos_set = set(input_data["photos"])
                input_photos = [
                    {"subject_id": input_data["subject_id"], "unique_id": id}
                    for id in input_photos_set
                ]
                db_input_data += input_photos
            for doc in db_input_data:
                await db[collection].delete_one(doc)

    @staticmethod
    async def delete_subject(subject_id: ObjectId):
        db = await get_db()
        await db[collection].delete_many({"subject_id": subject_id})
