from haystack.nodes import FARMReader, PreProcessor, PDFToTextConverter, DensePassageRetriever
from haystack.nodes import BM25Retriever
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines import ExtractiveQAPipeline
from haystack import Pipeline


async def  init_chat():
    
    document_store = InMemoryDocumentStore(use_bm25=True)

    preprocessor =  PreProcessor(
        clean_whitespace=True,
        clean_header_footer=True,
        clean_empty_lines=True,
        split_by="word",
        split_length=100,
        split_overlap=3,
        split_respect_sentence_boundary=True,
    )

    reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)
    retriever_es = BM25Retriever(document_store=document_store)
    pipe = ExtractiveQAPipeline(reader, retriever_es)

    pdf_file="./pdf2.pdf"
    converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["es"])
    document = [converter.convert(file_path=pdf_file, meta=None)[0]]
    preprocessed_docs = preprocessor.process(document)
    document_store.write_documents(preprocessed_docs)

    
    return pipe

