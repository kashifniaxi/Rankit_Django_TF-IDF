import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
from django.http import JsonResponse
from bs4 import BeautifulSoup
from django.shortcuts import render
import math




from home.models import Page
# Retrieve all objects from the model
def viewPage():
    all_objects = Page.objects.all()
    print(all_objects)
viewPage()
# strings = []
# # Access the column data for each object
# for obj in all_objects:
#     strings.append(obj.content)

# print(strings)






























nltk.download('stopwords')
# Create your views here.
def index(request):
    return render(request, 'index.html')
def search_result(request):
    return render(request, 'search_result.html')
def view_page(request):
    return render(request, 'view_page.html')

def highlight_query(query, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all text nodes within the HTML
    text_nodes = soup.find_all(text=True)

    for node in text_nodes:
            # Check if the query exists in the text node
        if query in node:
                # Create a new span element with highlighted style
            span = soup.new_tag('span', style='background-color: yellow;')
            span.string = query
            
            # Replace the query within the text node with the highlighted span element
            node.replace_with(node.replace(query, str(span)))

    highlighted_html = str(soup)
    return highlighted_html

# Create a SpellChecker object
spell_checker = SpellChecker()

# Function to provide spelling suggestions for a misspelled word
def get_spelling_suggestions(word):
    # Get a list of suggestions for the misspelled word
    suggestions = spell_checker.candidates(word)
    return suggestions


def get_suggestions(request, suggestions):
    # Get the query parameter from the request
    query = request.GET.get('query', '')

    suggestions = get_spelling_suggestions(query)

    # Filter the suggestions based on the query
    filtered_suggestions = [suggestion for suggestion in suggestions if query.lower() in suggestion.lower()]

    # Prepare the JSON response
    response = {
        'suggestions': filtered_suggestions
    }

    # Return the response as JSON
    return JsonResponse(response)









# Function to correct a query by replacing a misspelled word with the most likely suggestion
def correct_query(query):
    # Split the query into individual words
    words = query.split()

    # Iterate over each word and check if it is misspelled
    for i, word in enumerate(words):
        if not spell_checker.correction(word) == word:
            # If the word is misspelled, get the most likely suggestion
            corrected_word = spell_checker.correction(word)
            # Replace the misspelled word with the suggestion
            words[i] = corrected_word

    # Join the corrected words back into a single string
    corrected_query = " ".join(words)
    return corrected_query














# Preprocessing
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation marks
    text = "".join([char for char in text if char.isalnum() or char.isspace()])
    return text

# Tokenization and stopword removal
def tokenize_and_remove_stopwords(text):
    text = preprocess_text(text)
    # Tokenize the text into individual words
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

























tokenized_strings = [
    ['shipment', 'gold', 'damaged', 'gold'],
    ['delivery', 'silver', 'arrived','blue' 'silver'],
    ['shipment', 'gold', 'arrived', 'truck'],
]

# Example query
query = ['gold', 'silver', 'truck']

# Function to calculate term frequency (TF) for a given tokenized string
def calculate_tf(tokenized_string, term):
    return tokenized_string.count(term)

# Function to calculate inverse document frequency (IDF) for a given term in the tokenized strings
def calculate_idf(term):
    num_documents_with_term = sum(term in string for string in tokenized_strings)
    if num_documents_with_term > 0:
        return math.log(len(tokenized_strings) / num_documents_with_term)
    else:
        return 0.0

# Function to calculate the term vector for a given tokenized string and query
def calculate_term_vector(tokenized_string, query):
    term_vector = {}

    # Calculate TF-IDF for tokenized string terms
    for term in tokenized_string:
        tf = calculate_tf(tokenized_string, term)
        idf = calculate_idf(term)
        term_vector[term] = tf * idf

    return term_vector

# Calculate term vectors for each tokenized string and the query
# tokenized_string_term_vectors = [calculate_term_vector(string, query) for string in tokenized_strings]
# query_term_vector = calculate_term_vector(query, query)

# Function to calculate the cosine similarity between two vectors
def calculate_cosine_similarity(vector1, vector2):
    dot_product = sum(vector1.get(term, 0) * vector2.get(term, 0) for term in set(vector1) & set(vector2))
    magnitude_vector1 = math.sqrt(sum(value ** 2 for value in vector1.values()))
    magnitude_vector2 = math.sqrt(sum(value ** 2 for value in vector2.values()))
    if magnitude_vector1 > 0 and magnitude_vector2 > 0:
        return dot_product / (magnitude_vector1 * magnitude_vector2)
    else:
        return 0.0

# # Calculate cosine similarity between each tokenized string and the query
# string_scores = [(i, calculate_cosine_similarity(string_vector, query_term_vector)) for i, string_vector in enumerate(tokenized_string_term_vectors)]

# # Rank the tokenized strings based on the cosine similarity scores
# ranked_strings = sorted(string_scores, key=lambda x: x[1], reverse=True)

# # Print the ranked tokenized strings
# for string_index, score in ranked_strings:
#     print(f"Tokenized String {string_index+1}: {tokenized_strings[string_index]} (Score: {score})")








































# highlighted_html = highlight_query(query, html_content)
# print(highlighted_html)
