from google.cloud import storage
from pathlib import Path
import sys

index_path = Path('index.csv')
download_dir = Path('weights/')

print("Connecting to Google Cloud")

key_path = list(Path('.').glob('*.json'))[0]
storage_client = storage.Client.from_service_account_json(key_path)

bucket = storage_client.bucket('vit_models')

print("Finding Blobs")
names = [blob.name for blob in bucket.list_blobs()]
def find_name(partial):
    for name in names:
        if partial in name:
            return name
print("Found", len(names), "blobs")

index_blob = bucket.blob('augreg/index.csv')
index_blob.download_to_filename(index_path)

lines = index_path.open('r').readlines()
filenames = set([line.strip("\n").split(',')[-2] for line in lines])
for filename in filenames:
    partial_name = filename + '.npz'
    blob_name = find_name(partial_name)
    if blob_name is None:
        continue

    blob = bucket.blob(blob_name)
    download_path = Path(download_dir, partial_name)
    blob.download_to_filename(download_path)
    print(blob_name)

