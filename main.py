from flask import Flask, request, jsonify;
from flask_cors import cross_origin


from haystack.nodes import FARMReader, PreProcessor, PDFToTextConverter, DensePassageRetriever
from haystack.nodes import BM25Retriever
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines import ExtractiveQAPipeline
from haystack import Pipeline
from chat import init_chat 


app = Flask(__name__)



@app.route('/chat_bot', methods = ['POST'])
@cross_origin()
def chat(request):
    if request.method == 'POST':
        message_send = request.get_json()
        
        return jsonify({'message': result.get('answers')[0].answer})
    

async def main():
    await init_chat()


if __name__ == "__main__":
    main()
    app.run(debug=True)

