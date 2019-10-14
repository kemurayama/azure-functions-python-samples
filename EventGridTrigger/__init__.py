import os
import json
import logging
import aiofiles
import azure.functions as func
from azure.storage.blob.aio import BlobClient

async def main(event: func.EventGridEvent):
    result = json.dumps({
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
    })

    logging.info('Python EventGrid trigger processed an event: %s', result)
    result = json.loads(result)

    data = result['data']
    url = data['url']
    url = url.split('/')

    connection = os.environ['STORAGE']
    container = url[-2]
    filename = url[-1]

    
    async with BlobClient.from_connection_string(connection, container_name=container, blob_name=filename) as blob:
        stream = await blob.download_blob()
        data = await stream.content_as_bytes()
        async with aiofiles.open("./BlockDestination.txt", "wb") as my_blob:
            await my_blob.write(data)
            logging.info('finishied download my blob')