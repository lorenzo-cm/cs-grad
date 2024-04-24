from openai import OpenAI
from dotenv import load_dotenv
import os
from pdfminer.high_level import extract_text
from scipy import spatial
import pandas as pd

import numpy as np
from scipy.spatial import distance

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

MODEL = "text-embedding-3-small"


# ------------------------------
# Core functions
# ------------------------------

def extract_text_chunks(text, chunk_size, overlap):
    chunks = []
    start = 0
    while start + chunk_size < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap  # Move start up by chunk size minus overlap
    chunks.append(text[start:])  # Add the last chunk
    return chunks


def get_pdf_from_path(path: str) -> pd.DataFrame:
    # Extract text from PDF
    text = extract_text(path)

    # Remove any isolated '\n' characters that might be interpreted as new lines
    cleaned_text = text.replace('\n', ' ')

    # Break the text into 500-letter chunks with 100-letter overlap
    chunks = extract_text_chunks(cleaned_text, 500, 100)

    # Create a DataFrame from the chunks
    df = pd.DataFrame(chunks, columns=['text'])

    return df


def get_embbeding(client, input:str) -> list[int]:
    return client.embeddings.create(input=input, model=MODEL).data[0].embedding


def get_df_embedding(path:str) -> pd.DataFrame:
    df = get_pdf_from_path(path)
    client = OpenAI()

    df['embedding'] = df['text'].apply(lambda x: get_embbeding(client, x))
    return df


def strings_ranked_by_relatedness(query: str, df: pd.DataFrame, top_n: int = 5) -> tuple[list[str], list[float]]:
    """Returns a list of strings and relatednesses, sorted from most related to least."""
    client = OpenAI()
    
    query_embedding = get_embbeding(client, query)
    
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y)
    
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in df.iterrows()
    ]
    
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]


def format_prompt(useful_data:list, additional_context:dict={}):
    pdf_useful_data_formatted = f"""
    Use os textos abaixos sobre o hotel e as informações adicionais para responder de maneira direta e sem prolixidade à pergunta sequente. Se a resposta não for encontrada, responda que não sabe de uma maneira formal e criativa.
    
    Caso o prompt/requisição peça para resumir, sumarizar ou pergunte o conteúdo do texto ou do pdf, sumarize os textos obtidos.

    Textos:
    \"\"\"
    {str(useful_data)}
    \"\"\"
    
    Contexto adicional:
    {str(additional_context)}
    """

    return pdf_useful_data_formatted


def get_answer_embedding(prompt:str, useful_data:list, additional_context:dict={}):
    
    pdf_useful_data_formatted = format_prompt(useful_data, additional_context)
    
    client = OpenAI()
    
    model = 'gpt-3.5-turbo-0125'
    
    messages = [
        {"role": "system", "content": f"{pdf_useful_data_formatted}"},
        {"role": "user", "content": prompt},
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.6
    )
    
    response_message = response.choices[0].message.content
    return response_message



# ------------------------------
# Adapt the previous embedding 
# ------------------------------

def save_embedding(id:str) -> pd.DataFrame:
    """
    Saves the embedding
    
    Args:
        hotel_name (str): the hotel name. It should match exactly with the name in the pdf
    
    Returns:
        pd.Dataframe: dataframe with two cols, text and embeddings
    """
    
    path = f"../data/pdf/{id}/{id}.pdf"
    
    df = get_df_embedding(path)
    

    if not os.path.exists('../data/embeddings'):
        os.makedirs('../data/embeddings')
        
    try:
        df.to_parquet(f'../data/embeddings/{id}.parquet')
    except Exception as e:
        print(f"Error saving file: {e}")
    
    return df


def load_embedding(id:str) -> pd.DataFrame:
    """
    Load and return pd.Dataframe containing embeddings for the specified hotel.

    Args:
        hotel_name (str): Name of the hotel for which embeddings were generated and saved.

    Returns:
        pd.Dataframe: dataframe with two cols, text and embeddings

    Raises:
        FileNotFoundError: If the paquet file for the given hotel_name does not exist.
    """
    if not os.path.exists(f'../data/embeddings/{id}.parquet'):
        raise FileNotFoundError(f'Load embedding trying to open not existing file: "{id}.parquet"')

    df = pd.read_parquet(f'../data/embeddings/{id}.parquet')
    
    return df


def load_save_embedding(id, force_saving=False) -> pd.DataFrame:
    """
    Load the pd.Dataframe containing embeddings for the specified hotel if it exists, 
    otherwise generate and save embeddings

    Args:
        hotel_name: Name of the hotel for which embeddings were generated and saved (str)

    Returns:
        pd.Dataframe: dataframe with two cols, text and embeddings
    """
    path_embedding = f'../data/embeddings/{id}.parquet'
    
    if os.path.exists(path_embedding) and not force_saving:
        print("\n\n\n LOADANDO")
        return load_embedding(id)
    else:
        print("\n\n\n SALVANDO")
        return save_embedding(id)


def run_embeddings(id, prompt:str, additional_context={}, force_saving=False) -> tuple[str, list]:
    """
    Given a FAISS index `db`, a `prompt_template` string, a list of `input_variables`, a dictionary of `partial_variables`,
    and a `query` string, returns a list of responses generated by a GPT-3 model, as well as a list of source documents
    that were used to retrieve the information.

    Args:
        prompt (str)
        hotel_name (str)

    Returns:
        A tuple containing the generated response string and a list of source documents.
    """
    df = load_save_embedding(id, force_saving)
    useful_data, _ = strings_ranked_by_relatedness(prompt, df)
    print(useful_data)
    answer = get_answer_embedding(prompt, useful_data, additional_context)
    return answer, useful_data