import os
import logging
import datetime as dt
import azure.functions as func
from azure.identity.aio import ManagedIdentityCredential
from azure.storage.blob.aio import BlobClient

msi = None
expire_datetime = None

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    container = req.params.get('container')
    filename = req.params.get('file')
    if not filename:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            container = req_body.get('container')
            filename = req_body.get('file')

    STORAGE = os.environ['STORAGE']
    # Get Credentials from Web App
    global msi
    global expire_datetime
    if msi is None or expire_datetime < dt.datetime.now():
        msi = ManagedIdentityCredential(scopes=STORAGE)
        expire_datetime = dt.datetime.now() + dt.timedelta(hours=1)
        logging.info(f"Acquired token for {STORAGE}. Will expire at {expire_datetime.strftime('%Y/%m/%d %H:%M:%S')}")

    # Download file with BlobClient
    async with BlobClient(STORAGE, container, filename, credential= msi) as blob:
        stream = await blob.download_blob()
        data = await stream.content_as_bytes()
        logging.info('finishied download my blob')

    if filename and container:
        return func.HttpResponse(f"finished download blob {filename} from {container}")
    else:
        return func.HttpResponse(
             "Please pass a container and file on the query string or in the request body",
             status_code=400
        )
