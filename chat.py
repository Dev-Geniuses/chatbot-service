from haystack.nodes import FARMReader, PreProcessor, PDFToTextConverter, DensePassageRetriever
from haystack.nodes import BM25Retriever
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines import ExtractiveQAPipeline
from haystack import Pipeline


async def  init_chat():

    document_store = await InMemoryDocumentStore(use_bm25=True)

    preprocessor = await PreProcessor(
        clean_whitespace=True,
        clean_header_footer=True,
        clean_empty_lines=True,
        split_by="word",
        split_length=100,
        split_overlap=3,
        split_respect_sentence_boundary=True,
    )

    reader = await FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)
    retriever_es = await BM25Retriever(document_store=document_store)
    pipe = await ExtractiveQAPipeline(reader, retriever_es)

    pdf_file="./pdf2.pdf"
    converter = await PDFToTextConverter(remove_numeric_tables=True, valid_languages=["es"])
    document = await [converter.convert(file_path=pdf_file, meta=None)[0]]
    preprocessed_docs = await preprocessor.process(document)
    await document_store.write_documents(preprocessed_docs)

    question= "Qué es un informe académico?"

    result = await pipe.run(
            query=question, 
            params={
                "Retriever": {"top_k": 10},
                "Reader": {"top_k": 5}
            })

    print(result.get('answers')[0].answer) 

