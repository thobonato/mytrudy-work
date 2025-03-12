from openai import OpenAI
from typing import List, Union, Optional, Dict, Any
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

class Embedder:
    def __init__(self, model: str = "text-embedding-3-small"):
        """
        Initialize the OpenAI embedder.
        
        Args:
            model: The OpenAI embedding model to use. Default is text-embedding-3-small.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = model
        
    def get_embedding(self, text: Union[str, List[str]]) -> dict:
        """
        Get embeddings for a single text string or multiple text strings.
        
        Args:
            text: The text to embed (string or list of strings)
            
        Returns:
            A dictionary containing the embedding vector(s), total time, and time per embedding
        """
        start_time = time.time()
        
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Handle single string case
        if isinstance(text, str):
            return {
                "embedding": response.data[0].embedding,
                "total_time": total_time,
                "time_per_embedding": total_time
            }
        # Handle list of strings case
        else:
            time_per_embedding = total_time / len(text)
            return {
                "embeddings": [item.embedding for item in response.data],
                "total_time": total_time,
                "time_per_embedding": time_per_embedding
            }
    
    def create_batch_embeddings(self, input_file_id: str, completion_window: str = "24h", metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a batch embedding job using OpenAI's Batch API.
        
        Args:
            input_file_id: The ID of the input file containing texts to embed
            completion_window: Time window for batch completion (default: "24h")
            metadata: Optional metadata for the batch job
            
        Returns:
            The batch ID
        """
        try:
            batch = self.client.batches.create(
                input_file_id=input_file_id,
                endpoint="/v1/embeddings",
                model=self.model,
                completion_window=completion_window,
                metadata=metadata or {"description": f"Batch embeddings using {self.model}"}
            )
            return batch.id
        except Exception as e:
            print(f"Error creating batch: {str(e)}")
            raise
    
    def get_batch_status(self, batch_id: str) -> Dict[str, Any]:
        """
        Check the status of a batch embedding job.
        
        Args:
            batch_id: The ID of the batch job to check
            
        Returns:
            Dictionary containing batch status information
        """
        try:
            batch = self.client.batches.retrieve(batch_id)
            return {
                "status": batch.status,
                "created_at": batch.created_at,
                "expires_at": batch.expires_at,
                "total_requests": batch.total_requests,
                "succeeded_requests": batch.succeeded_requests,
                "failed_requests": batch.failed_requests
            }
        except Exception as e:
            print(f"Error retrieving batch status: {str(e)}")
            raise
    
    def get_batch_results(self, file_id: str) -> str:
        """
        Retrieve results from a completed batch embedding job.
        
        Args:
            file_id: The ID of the output file containing embeddings
            
        Returns:
            The content of the results file
        """
        try:
            file_response = self.client.files.content(file_id)
            return file_response.text
        except Exception as e:
            print(f"Error retrieving batch results: {str(e)}")
            raise
    
    def cancel_batch(self, batch_id: str) -> bool:
        """
        Cancel a batch embedding job.
        
        Args:
            batch_id: The ID of the batch job to cancel
            
        Returns:
            True if cancellation was successful, False otherwise
        """
        try:
            self.client.batches.cancel(batch_id)
            return True
        except Exception as e:
            print(f"Error canceling batch: {str(e)}")
            return False
    
    def list_batches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        List recent batch embedding jobs.
        
        Args:
            limit: Maximum number of batches to return (default: 10)
            
        Returns:
            List of batch information dictionaries
        """
        try:
            batches = self.client.batches.list(limit=limit)
            return [{
                "id": batch.id,
                "status": batch.status,
                "created_at": batch.created_at,
                "total_requests": batch.total_requests
            } for batch in batches.data]
        except Exception as e:
            print(f"Error listing batches: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    import json
    
    load_dotenv()
    
    # Regular embedding example
    sample_text = "This is a test sentence to embed."
    embedder = Embedder()
    result = embedder.get_embedding(sample_text)
    
    print("Regular Embedding Example:")
    print(f"Embedding dimension: {len(result['embedding'])}")
    print(f"Total time: {result['total_time']:.4f} seconds\n")
    
    # Batch processing example
    print("Batch Processing Example:")
    try:
        # List recent batches
        print("\nRecent batches:")
        batches = embedder.list_batches(limit=5)
        for batch in batches:
            print(f"Batch {batch['id']}: {batch['status']}")
        
        # Note: To use batch processing, you would first need to upload your input file
        # and get its file_id. Then you can use it like this:
        """
        batch_id = embedder.create_batch_embeddings(
            input_file_id="your_file_id",
            metadata={"description": "My batch embedding job"}
        )
        
        # Check status
        status = embedder.get_batch_status(batch_id)
        while status["status"] != "completed":
            time.sleep(60)  # Check every minute
            status = embedder.get_batch_status(batch_id)
        
        # Get results when complete
        results = embedder.get_batch_results("output_file_id")
        print(f"\nFirst few results: {results[:100]}")
        """
        
    except Exception as e:
        print(f"Error in batch processing example: {str(e)}")
