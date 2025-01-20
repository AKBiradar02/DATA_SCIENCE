import os
import re
import sys
import pandas as pd
import nltk
import openpyxl
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import requests
from collections import Counter
from textstat import textstat


# Ensuring required resources are installed
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

# Load the stopwords.
stop_words = set(stopwords.words('english'))

# placeholder for positive and negative word dictonaries.
positive_words = set()
negative_words = set()

# Load the positive and negative words from external files(xlsx)
with open('C:\\Users\\abhay\\OneDrive\\Desktop\\Text_Analysis_overview\\MasterDictionary\\negative-words.txt', 'r') as f:
    negative_words = set(f.read().splitlines())

with open('C:\\Users\\abhay\\OneDrive\\Desktop\\Text_Analysis_overview\\MasterDictionary\\positive-words.txt', 'r') as f:
    positive_words = set(f.read().splitlines())


def clean_text(text):
    """" remove the input text by removing stop words and puntuations"""
    tokens = word_tokenize(text)
    cleaned_tokens = [word for word in tokens if word.lower()
                      not in stop_words and word.isalpha()]
    return cleaned_tokens


def calculate_scores(tokens):
    """"Calculating positiive, negative, polarity, and subjectivity scores"""
    positive_score = sum(1 for words in tokens if words in positive_words)
    negative_score = sum(1 for words in tokens if words in negative_words)

    polarity_score = (positive_score - negative_score) / \
        ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / \
        (len(tokens) + 0.000001)

    return positive_score, negative_score, polarity_score, subjectivity_score


def analyze_readability(text):
    """"Calculating readability scores"""
    average_sentence_length = len(
        word_tokenize(text)) / len(sent_tokenize(text))
    percentange_complex_words = calculate_complex_word_count(
        text) / len(word_tokenize(text))
    fog_index = 0.4*(average_sentence_length + percentange_complex_words)

    return average_sentence_length, percentange_complex_words, fog_index


def calculate_complex_word_count(text):
    """Calculating the number of complex words in the text"""
    tokens = word_tokenize(text)
    complex_words = [word for word in tokens if count_syllables(word) > 2]
    return len(complex_words)


def count_syllables(word):
    """Calculating the number of syllables in a word"""
    word = word.lower()
    vowels = 'aeiou'
    syllable_count = sum(1 for char in word if char in vowels)
    if word.endswith(('es', 'ed', 'e')):
        syllable_count -= 1

    return max(syllable_count, 1)


def count_personal_pronouns(text):
    """Counting the number of personal pronouns in the text"""
    pronouns = re.findall(r'\b(?:I|we|my|ours|us)\b', text, re.IGNORECASE)

    return len(pronouns)


def calculate_average_word_length(tokens):
    """Calculating the average word length in the text"""
    total_characters = sum(len(word) for word in tokens)
    return total_characters / len(tokens)


def extract_text_from_url(url):
    """Extracting text from a URL"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # cusomising based on the structure of your target pages
        title = soup.title.string if soup.title else ""
        paragraphs = soup.find_all('p')
        content = ' '.join(paragraph.text for paragraph in paragraphs)
        return f"{title}\n{content}"
    except Exception as e:
        print(f"Error Fetching {url}: {e}")
        return ""


def analyze_text(text):
    """Analyzing the text"""
    cleaned_tokens = clean_text(text)
    positive_score, negative_score, polarity_score, subjectivity_score = calculate_scores(
        cleaned_tokens)
    average_sentence_length, percentange_complex_words, fog_index = analyze_readability(
        text)
    complex_word_count = calculate_complex_word_count(text)
    word_count = len(cleaned_tokens)
    syllable_count_per_word = sum(count_syllables(word)
                                  for word in cleaned_tokens) / word_count

    personal_pronoun_count = count_personal_pronouns(text)
    average_word_length = calculate_average_word_length(cleaned_tokens)

    return {
        "positive_score": positive_score,
        "negative_score": negative_score,
        "polarity_score": polarity_score,
        "subjectivity_score": subjectivity_score,
        "average_sentence_length": average_sentence_length,
        "percentange_complex_words": percentange_complex_words,
        "fog_index": fog_index,
        "complex_word_count": complex_word_count,
        "word_count": word_count,
        "syllable_count_per_word": syllable_count_per_word,
        "personal_pronoun_count": personal_pronoun_count,
        "average_word_length": average_word_length
    }


def process_urls(input_file, output_file, output_format):
    """Processing the URLs from the input file and writing the results to the output file"""
    # read input file
    df = pd.read_excel(
        'C:\\Users\\abhay\\OneDrive\\Desktop\\Text_Analysis_overview\\Input.xlsx')
    # process each URL
    results = []
    for index, row in df.iterrows():
        url = row.get('URL')
        url_id = row.get('URL_ID')
        if url:
            print(f"Processing {url}")
            text = extract_text_from_url(url)
            if text:
                analysis = analyze_text(text)
                analysis["URL_ID"] = url_id
                analysis["URL"] = url
                results.append(analysis)

    # write results to output file
    output_df = pd.DataFrame(results)

    #reorder columns to have URL ID first, followed by URL, and then the metrics
    columns_order = ["URL_ID", "URL"] + [col for col in output_df.columns if col not in ["URL ID", "URL"]]
    output_df = output_df[columns_order]

    if output_format == 'csv':
        output_df.to_csv(output_file, index=False)
    elif output_format == 'excel':
        output_df.to_excel(output_file, index=False)
    else:
        print("Invalid output format. Please use 'csv' or 'excel'.")

    print(f"\nResults written to {output_file}")
    return output_df


# Example usage
if __name__ == '__main__':
    input_file = 'C:\\Users\\abhay\\OneDrive\\Desktop\\Text_Analysis_overview\\Input.xlsx'
    output_file = 'C:\\Users\\abhay\\OneDrive\\Desktop\\Text_Analysis_overview\\Output.xlsx'
    output_format = 'excel'
    process_urls(input_file, output_file, output_format)

# # Example usage
# if __name__ == '__main__':
#     input_file = 'C:\\Users\\abhay\\OneDrive\\Desktop\\Text_An
#     output_file = 'C:\\Users\\abhay\\OneDrive\\Desktop\\Text_Analysis_overview\\Output.xlsx'
#     output_format = 'excel'
#     process_urls(input_file, output_file, output_format)
