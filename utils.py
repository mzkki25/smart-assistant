import pdfplumber
import spacy
import os
import numpy as np

from gradio_client import Client, handle_file
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def revise_the_sentence(prompt, system):
    try:
        client = Client("Qwen/Qwen2-72B-Instruct")
        result = client.predict(
            query=prompt,
            history=[],
            system=system,
            api_name="/model_chat"
        )
        return result[1][0][1]
    
    except Exception as e:
        return "Error: " + str(e)

def load_pdf_text(file_path: str):
    """
    Reads a PDF file and returns its text content.
    
    :param file_path: Path to the PDF file.
    :return: Text content of the PDF file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    
    return text.strip()

def chunk_text(text, max_words):
    words = text.split()

    if len(words) <= max_words:
        return [text]
    
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)
    
    return chunks

def embed_chunks(chunks, model):
    return model.encode(chunks)

def retrieve_best_chunk(query, chunks, chunk_embeddings, model):
    query_embedding = model.encode([query])
    scores = cosine_similarity(query_embedding, chunk_embeddings)[0]
    best_idx = scores.argmax()
    return chunks[best_idx]

def image_capt(img_path):
    client = Client("tonyassi/blip-image-captioning-large")
    result = client.predict(
        img=handle_file(img_path),
        min_len=50,
        max_len=350,
        api_name="/predict"
    )

    result = ' '.join(result.split()[:-2])
    return result

def extract_tags(caption, top_n=5):
    doc = nlp(caption.lower())
    tags = [token.lemma_ for token in doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop]
    unique_tags = list(dict.fromkeys(tags)) 
    return unique_tags[:top_n]