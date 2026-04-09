from .mapper import map_product_to_document
import time,requests,json
from ..Settings.SecretSettings import settings
from ..Models.ProductModel import Product
from typing import List
from decimal import Decimal


AUTH_HEADER = {
    "Authorization": f"Bearer {settings.coveo_api_key}",
    "Content-Type": "application/json"
}


def create_file_container():
    url = f"https://api.cloud.coveo.com/push/v1/organizations/{settings.coveo_org_id}/files"

    res = requests.post(url, headers=AUTH_HEADER)
    res.raise_for_status()

    data = res.json()

    return (
        data["uploadUri"],
        data["fileId"],
        data["requiredHeaders"]
    )



# 3. Upload batch to S3
def upload_batch(upload_uri, required_headers, payload):
    headers = {
        "x-amz-server-side-encryption": required_headers["x-amz-server-side-encryption"],
        "Content-Type": required_headers["Content-Type"]
    }

    res = requests.put(
        upload_uri,
        headers=headers,
        data=json.dumps(
            payload,
            default=lambda x:float(x) if isinstance(x,Decimal) else x).encode("utf-8")
    )

    res.raise_for_status()



# 4. Push batch to Coveo
def push_batch(file_id):
    url = f"https://api.cloud.coveo.com/push/v1/organizations/{settings.coveo_org_id}/sources/{settings.coveo_source_id}/documents/batch?fileId={file_id}"

    res = requests.put(url, headers=AUTH_HEADER)
    res.raise_for_status()



def push_products(products:List[Product]):

    print(type(len(products)))
    for i in range(0, len(products), settings.coveo_batch_size):
        batch = products[i:i + settings.coveo_batch_size]

        documents = [map_product_to_document(p) for p in batch]
        payload = {
            "addOrUpdate": documents,
            "delete": []
        }
        upload_uri, file_id, required_headers = create_file_container()
        upload_batch(upload_uri, required_headers, payload)
        push_batch(file_id)
        print(f"Pushed batch {i //  settings.coveo_batch_size + 1}")
        # time.sleep(3)





