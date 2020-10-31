import os
import logging
import datetime as dt
import azure.functions as func
from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobClient

msi = None
expire_datetime = None

async def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
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
        
        # Get Credentials from Function App
        global msi
        global expire_datetime
        if msi is None or expire_datetime < dt.datetime.now():
            msi = DefaultAzureCredential()
            expire_datetime = dt.datetime.now() + dt.timedelta(hours=1)
            logging.info(f"Acquired token for Storage Account. Will expire at {expire_datetime.strftime('%Y/%m/%d %H:%M:%S')}")
        
        STORAGE_NAME = os.environ.get('STORAGE_NAME')

        # Download file with BlobClient
        async with BlobClient(STORAGE_NAME, container, filename, credential= msi) as blob:
            stream = await blob.download_blob()
            data = await stream.content_as_text()
            logging.info(f'finishied download file. insde data is "{data}"')
            return func.HttpResponse(f"finished download blob {filename} from {container}")

    except Exception as e:
        logging.exception(f'Failed to download file:{e}')
        return func.HttpResponse(
             "Please pass a container and file on the query string or in the request body",
             status_code=400
        )
