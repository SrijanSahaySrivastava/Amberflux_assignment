# Assignment from AmberFlux
## FastAPI application to store images in Vector DB(Qdrant)

### Requirements
-   Python
-   Docker (Qdrant up and running)

### Qdrant Docker Setup

```bash
docker pull qdrant/qdrant
docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant
```
https://qdrant.tech/documentation/quickstart/


### How to Run

create env (I used `uv`)
```bash
uv venv
.venv/bin/activate
```


Install Dependencies
```bash
uv pip install -r requirements.txt
```

Run FastAPI server
```bash
uvicorn main:app
```

### How to Request

#### Upload:
requires .mp4 file
```python
import requests

collection_name = "<collection_name>"
url = f"http://127.0.0.1:8000/upload_video/?collection_name={collection_name}"

payload = {'host': 'http://localhost:6333'}
files=[
  ('file',('<file_name.mp4>',open('<file_path.mp4>','rb'),'application/octet-stream'))
]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)

```

#### search:
required .jpg image to search the DB
```python
import requests

collection_name = "<collection_name>"
url = f"http://127.0.0.1:8000/upload_video/?collection_name={collection_name}"

payload = {'host': 'http://localhost:6333',
'limit': '5'}
files=[
  ('image',('<file_name.jpg>',open('<file_path.jpg>','rb'),'image/jpeg'))
]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
```
sample response:
```json
{
    "results": {
        "points": [
            {
                "id": 778,
                "version": 1703,
                "score": 1.0,
                "payload": {
                    "image_path": "frame8.jpg"
                },
                "vector": null,
                "shard_key": null,
                "order_value": null
            }
        ]
    }
}
```

### contact: 
srijansahaysri13@gmail.com