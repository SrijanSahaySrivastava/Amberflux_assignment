from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from frames import computer_vector, computer_vector_from_path
import os

collection_name = 'test'
dimensions = 2048
metric = Distance.COSINE

def setup_collection(collection_name, dimensions, metric, host="http://localhost:6333"):
    
    client = QdrantClient(url="http://localhost:6333")
    try:
        client.get_collection(collection_name=collection_name)
    except Exception as e:
        print(f"Collection {collection_name} does not exist. Creating a new one. Error: {e}")
        client.create_collection(
                collection_name = collection_name,
                vectors_config = VectorParams(
                    size = dimensions, 
                    distance = metric
                ),
        )

def insert_points(base_dir, collection_name, host="http://localhost:6333"):
    client = QdrantClient(url=host)
    vectors = computer_vector(base_dir)
    if vectors.size == 0:
        raise ValueError("No vectors found. Please check the image paths.")
    points = []
    frames_dir = os.path.join(base_dir, "Frames")
    image_names = sorted([f for f in os.listdir(frames_dir) if f.endswith('.jpg')])
    
    for i, vector in enumerate(vectors):
        flat_vector = vector.flatten().tolist()
        point = PointStruct(
            id=i,
            vector=flat_vector,
            payload={
                "image_path": image_names[i]
            }
        )
        # Upsert the point individually
        client.upsert(
            collection_name=collection_name,
            points=[point]
        )
        print(f"Upserted point {i}")
        
def search_points(collection_name, query_image_path, limit=5, host="http://localhost:6333"):
    client = QdrantClient(url=host)
    query_vector = computer_vector_from_path(query_image_path)
    results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=limit
    )
    return results


# setup_collection(collection_name, dimensions, metric)
# insert_points("files", collection_name)
# print(search_points(collection_name, "files/Frames/frame0.jpg", limit=5))
# print(client.get_collection(collection_name=collection_name).points_count)
