import requests
import re
from typing import List

'''
def llama_3_3(messages, temperature=0.7, timeout=600):

    url = 'http://140.119.112.78:65088/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'llama-3.3-70b',
        'messages': messages,
        'temperature': temperature
    }

    try:
        with requests.Session() as session:
            session.timeout = timeout
            response = session.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise an HTTPError if the response contains an HTTP error status code
            return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
'''

'''
def sent_cut_zh(para: str) -> List[str]:
    para = re.sub('([。！？\?!])([^”’)\]）】])', r"\1\n\2", para)
    para = re.sub('(\.{3,})([^”’)\]）】….])', r"\1\n\2", para)
    para = re.sub('(\…+)([^”’)\]）】….])', r"\1\n\2", para)
    para = re.sub('([。！？\?!]|\.{3,}|\…+)([”’)\]）】])([^，。！？\?….])', r'\1\2\n\3', para)
    para = para.rstrip()
    sentences = para.split("\n")
    sentences = [sent.strip() for sent in sentences]
    sentences = [sent for sent in sentences if len(sent.strip()) > 0]
    return sentences
'''

def filter_text(para: str) -> str:
    """
    Filters out non-Chinese and non-English characters from the input string using regular expressions.

    Parameters:
        para (str): The input string to filter.

    Returns:
        str: The filtered string containing only Chinese and English characters.
    """
    return re.sub(r'[^\u4e00-\u9fa5a-zA-Z\s]', '', para)