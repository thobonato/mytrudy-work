# ------------------------------------------------------------
# Steps to setting up a vector db with MongoDB Atlas Search
# ------------------------------------------------------------
# 1. Create a new cluster in MongoDB Atlas
# 2. Enable Atlas Search
# 3. Create a new index
# 4. Setup necessary specs (number of dimensions, etc.)
# 5. Get connection string from MongoDB Atlas
# 6. Add vectors to the collection
# ------------------------------------------------------------

import pymongo
from pymongo import MongoClient
import numpy as np
from typing import List, Dict, Any, Optional

class VectorDatabase:
    def __init__(self, connection_string: str = "mongodb+srv://bonato:<db_password>@cluster0.motpw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"):
        """
        Initialize connection to MongoDB Atlas Vector Database.
        
        Args:
            connection_string: MongoDB connection string. Default is MongoDB Atlas.
        """
        # Ensure we're using pymongo[srv] for Atlas connections
        self.client = MongoClient(connection_string)
        self.db = self.client["vector-db"]
        self.collection = self.db["vector-coll"]
        
    def add_vector(self, user_id: str, text: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a vector to the collection.
        
        Args:
            user_id: Unique identifier for the user
            text: Original text that was embedded
            vector: The embedding vector
            metadata: Additional metadata to store with the vector
            
        Returns:
            The ID of the inserted document
        """
        document = {
            "userId": user_id,
            "text": text,
            "embedding": vector
        }
        
        if metadata:
            document["metadata"] = metadata
            
        result = self.collection.insert_one(document)
        return str(result.inserted_id)
    
    def query_similar(self, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Query the collection for vectors similar to the query vector.
        
        Args:
            query_vector: The vector to compare against
            limit: Maximum number of results to return
            
        Returns:
            List of documents sorted by similarity
        """
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_vector,
                    "limit": limit,
                    "numCandidates": limit * 10,
                    "exact": False
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "userId": 1,
                    "text": 1,
                    "metadata": 1,
                    "score": {
                        "$meta": "vectorSearchScore" 
                    }
                }
            }
        ]
        
        cursor = self.collection.aggregate(pipeline)
        results = list(cursor)
        print(f"Found {len(results)} results")
        for result in results:
            print(f"Result: {result}")
        return results
    
    def query_by_user_id(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Query the collection for documents with the given user ID.
        
        Args:
            user_id: The user ID to search for
            
        Returns:
            List of documents matching the user ID
        """
        results = list(self.collection.find({"userId": user_id}))

        return results
    
    def close(self):
        """Close the MongoDB connection"""
        self.client.close()

# ------------------------------------------------------------
# Example usage for MongoDB Atlas Vector Database
# ------------------------------------------------------------
if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    db_password = os.getenv("DB_PASSWORD")
    # Using my MongoDB Atlas connection string (already set up)
    str_connection = "mongodb+srv://bonato:" + db_password + "@cluster0.motpw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    db = VectorDatabase(str_connection)
    
    # create a random vector of 1536 dimensions
    num_dimensions = 1536
    vector = np.random.rand(num_dimensions).tolist()
    
    # Add vector
    # vector_id = db.add_vector("user1", "This is a test vector", vector)
    # print(f"Added vector with ID: {vector_id}")
    
    # Let mongo update the index
    import time
    time.sleep(1)
    
    # Query similar vectors
    print("\nQuerying for similar vectors...")
    query_vector = vector.copy()
    query_vector[0] += 0.15
    
    results = db.query_similar(query_vector)
    if results:
        print(f"\nFound {len(results)} similar vectors:")
        for idx, result in enumerate(results, 1):
            print(f"{idx}. {result}")
    else:
        print("No similar vectors found")
    
    