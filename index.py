import os
import re
from dotenv import load_dotenv
from db import MongoDBHandler
from ai import AIHandler
import json

load_dotenv()

dbHandler = MongoDBHandler(os.getenv("DB_CONNECTION_STRING"))

documents = dbHandler.query_documents({"status": "unprocessed"})

aiHandler = AIHandler()

for doc in documents:
    task = doc["task"]
    print(f"processing task: {task}")
    responseText = aiHandler.generateTaskResponse(task)
    print(f"AI response: {responseText}")

    try:
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", responseText.strip())
        responseDict = json.loads(cleaned)
        print(responseDict)
        dbHandler.update_document(doc["_id"], "skills", responseDict["skills"])
        if responseDict["message"]:
            dbHandler.update_document(doc["_id"], "message", responseDict["message"])
            dbHandler.update_document(doc["_id"], "status", "requires_clarification")
        else:
            dbHandler.update_document(doc["_id"], "status", "processed")

    except Exception as e:
        print(f"Error processing AI response for document {doc['_id']}: {e}")

dbHandler.close()