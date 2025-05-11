from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from frames import computer_vector
import os

collection_name = 'test'
dimensions = 2
metric = Distance.COSINE

def setup_collection(collection_name, dimensions, metric, host="http://localhost:6333"):
    
    client = QdrantClient(url="http://localhost:6333")
    try:
        client.get_collection(collection_name=collection_name)
        # Create a new collection
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
        print(f"Processing image {i+1}/{len(vectors)}: {image_names[i]}")
        flat_vector = vector.flatten().tolist()
        point = PointStruct(
            id=i,
            vector=flat_vector,
            payload={
                "image_path": image_names[i]
            }
        )
        points.append(point)
    print(f"Total points to insert: {len(points)}")
    
    client.upsert(
        collection_name=collection_name,
        points=points
    )

setup_collection(collection_name, 512, metric)
insert_points("files", collection_name)
# print(client.get_collection(collection_name=collection_name).points_count)
