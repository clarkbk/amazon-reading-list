import goodreads_api_client as gr
import os

key = os.environ['GOODREADS_API_KEY']
client = gr.Client(developer_key=key)
