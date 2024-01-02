# Import necessary libraries
import os
from nltk.corpus import stopwords
from nltk import PorterStemmer
from bs4 import BeautifulSoup
from nltk import word_tokenize
import re, json
from concurrent.futures import ThreadPoolExecutor

# Function to read the content of a file at the specified file path
def read_file_content(file_path):
    with open(file_path, 'r', errors="ignore") as file:
        return file.read()

# Function to extract news item from reuters text article 
def extract_text_from_article(article):
    title = ""
    paragraphs = ""

    article_title = article.find('title')
    if article_title:
        title = article_title.get_text().replace('\\n', '').replace('\n', '')

    article_body = article.find('body')
    if article_body:
        body_string = article_body.get_text().replace('\u0003', '').replace("\\", "")
        body_lines = body_string.split('\n')
        paragraphs = '\n'.join(body_lines)
    
    item_text = f"{title}\n\n{paragraphs}"

    return item_text

# Function to extract text from the Reuters corpus
def text_extraction(reuters_corpus):
    documents = []
    reuters_files = os.listdir(reuters_corpus)
    
    # Process each document in parallel using a thread pool
    def process_document(item):
        if item.endswith(".sgm"):
            item_path = os.path.join(reuters_corpus, item)
            content = read_file_content(item_path)
            
            soup = BeautifulSoup(content, 'html.parser')
            news_articles = soup.find_all('reuters')

            for article in news_articles:
                text_item = extract_text_from_article(article)
                documents.append((article['newid'], text_item))
    
    with ThreadPoolExecutor(max_workers=6) as executor:  
        executor.map(process_document, reuters_files)
    
    return documents

# Function to tokenize text
def Tokenizer(textList=None):
    TokenizedText_List = []
    token_pattern = re.compile(r'\b\w{3,}\b')

    for news_item in textList:
        id = news_item[0]
        tokensList = [token for token in word_tokenize(news_item[1]) if re.match(token_pattern, token)]
        TokenizedText_List.append((id, tokensList))
    return TokenizedText_List

# Function to convert tokens to lowercase
def Lowercased(tokensList=None):
    LowercasedTokens_list = []
    # Define a regular expression pattern to match numeric values
    for news_item in tokensList:
        id = news_item[0]
        # Filter out tokens that match the numeric pattern and convert to lowercase
        lowercasedTokens = [token.lower() for token in news_item[1]]
        LowercasedTokens_list.append((id, lowercasedTokens))
    return LowercasedTokens_list

# Function to stem tokens
def Stemmer(lowercaseTokensList=None):
    StemmedTokens_list = []
    stemmer = PorterStemmer()
    for news_item in lowercaseTokensList:
        id = news_item[0]
        stemmedTokens = [stemmer.stem(token) for token in news_item[1]]
        StemmedTokens_list.append((id, stemmedTokens))
    return StemmedTokens_list

# Function to remove stop words from tokens
def withoutStopWords(tokens_list=None, stop_words=None):
    FilteredTokens_list = []
    for news_item in tokens_list:
        id = news_item[0]
        filtered_list = [token for token in news_item[1] if token not in stop_words]
        FilteredTokens_list.append((id, filtered_list))
    return FilteredTokens_list

# Function to load an index from a JSON file
def load_index(index_path):
    with open(index_path, 'r') as index_file:
        index = json.load(index_file)
    return index

# Function to write an index to a JSON file
def write_index(path, index):
    with open(path, 'w') as file:
        json.dump(index, file)
