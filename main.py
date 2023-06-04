from flask import Flask, request, jsonify;
from flask_cors import cross_origin
import asyncio
import tracemalloc

from haystack.nodes import FARMReader, PreProcessor, PDFToTextConverter, DensePassageRetriever
from haystack.nodes import BM25Retriever
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines import ExtractiveQAPipeline
from haystack import Pipeline
from chat import init_chat


app = Flask(__name__)



global pipe

@app.route('/chat_bot', methods = ['POST'])
@cross_origin()
def chat():
    if request.method == 'POST':
        message_send = request.json.get('message')
        print(message_send)
        print(type(message_send))
        result = pipe.run(
            query=message_send, 
            params={
                "Retriever": {"top_k": 10},
                "Reader": {"top_k": 5}
            })

    return jsonify({'Answer': result.get('answers')[0].answer})
    

async def main():
   return await init_chat()
   

if __name__ == "__main__":

    pipe = asyncio.run(main())
    app.run(debug=True)

