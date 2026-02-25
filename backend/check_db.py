import os
import sys
from pymongo import MongoClient
from bson import ObjectId

# Get connection string from environment or use default
mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
db_name = os.environ.get('MONGODB_NAME', 'prompt_selector')

print(f"Connecting to MongoDB: {mongo_uri}")
print(f"Database: {db_name}")

try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    db = client[db_name]
    collection = db['api_prompt']
    
    # Get count
    count = collection.count_documents({})
    print(f"\nTotal documents in api_prompt collection: {count}")
    
    # Get the specific ID the user mentioned
    test_id = "699e6ef5568cc2f65a8fa04f"
    print(f"\nLooking for document with _id: {test_id}")
    
    doc = collection.find_one({'_id': ObjectId(test_id)})
    if doc:
        print(f"✓ Found document!")
        print(f"  Prompt: {doc.get('prompt_text', '')[:50]}...")
        print(f"  Has response_a: {bool(doc.get('response_a'))}")
        print(f"  Has response_b: {bool(doc.get('response_b'))}")
        print(f"  Preference: {doc.get('preference')}")
    else:
        print(f"✗ Document NOT found")
        
    # List last 5 document IDs
    print(f"\nLast 5 document IDs in collection:")
    for doc in collection.find().sort('_id', -1).limit(5):
        print(f"  {doc['_id']}")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
