import os
import json
import logging
from pathlib import Path
from urllib.parse import urlparse

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
    try:
        result = json.loads(result)

        data = result['data']
        url = urlparse(data['url'])
        p_file = Path(url.path)
        filename = p_file.name
        container = p_file.parent.name
        connection = os.environ['STORAGE_CONNECTION']

        async with BlobClient.from_connection_string(connection, container_name=container, blob_name=filename) as blob:
            stream = await blob.download_blob()
            data = await stream.content_as_text()
            logging.info(f'Content is {data}')

    except Exception as e:
        logging.exception(f"failed to load EventGrid request:{e}")
 