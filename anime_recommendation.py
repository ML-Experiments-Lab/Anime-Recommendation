import numpy as np
import pandas as pd
import re
from nltk.stem.porter import PorterStemmer
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process

# Load the dataset
anime = pd.read_csv("static/anime_dataset.csv")

# Data Cleaning
anime.fillna({
    'English Name': 'Unknown',
    'Producers': 'Unknown',
    'Theme': 'Unknown',
    'Rating': anime['Rating'].mean(),
    'Genres': 'Unknown',
    'Duration': 'Unknown',
    'Synopsis': 'Synopsis is not available',
    'Image source': 'Image preview not available'
}, inplace=True)

# Select needed columns
new_anime = anime[['Name', 'Synopsis', 'Genres', 'English Name', 'Image source', 'Rating', 'Duration', 'Theme', 'Producers']].copy()

# Text preprocessing
ps = PorterStemmer()

def stem(text):
    return " ".join([ps.stem(word) for word in text.split()])

for col in ['Genres', 'Synopsis', 'Theme', 'Producers']:
    new_anime[col] = new_anime[col].apply(lambda x: stem(x) if isinstance(x, str) else x)

# Convert duration to minutes
def convert_duration(duration):
    try:
        hours = re.search(r'(\d+)\s*hr', duration)
        minutes = re.search(r'(\d+)\s*min', duration)
        if 'sec' in duration:
            return 1
        return (int(hours.group(1)) * 60 if hours else 0) + (int(minutes.group(1)) if minutes else 0)
    except:
        return 0

new_anime['Duration'] = new_anime['Duration'].apply(convert_duration)

# Normalize numeric features
scaler = MinMaxScaler()
new_anime[['Rating', 'Duration']] = scaler.fit_transform(new_anime[['Rating', 'Duration']])

# Combine features
new_anime['combined_features'] = (
    (new_anime['Genres'] + " ") * 15 +
    (new_anime['Synopsis'] + " ") * 5 +
    (new_anime['Producers'] + " ") * 6 +
    (new_anime['Theme'] + " ") * 13 +
    (new_anime['Rating'].astype(str) + " ") * 15 +
    (new_anime['Duration'].astype(str) + " ") * 13
)

# TF-IDF and Model Fitting
tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
tfidf_matrix = tfidf.fit_transform(new_anime['combined_features'])

nn_model = NearestNeighbors(metric='cosine', algorithm='brute')
nn_model.fit(tfidf_matrix)

def load_models():
    return new_anime, nn_model, tfidf, tfidf_matrix

def get_recommendations(anime_title, top_n=20):
    anime_title = anime_title.strip().lower()
    print(f"Searching recommendations for: {anime_title}")

    best_match = process.extractOne(anime_title, new_anime['English Name'])
    print(f"Best match: {best_match}")

    if best_match is None or best_match[1] < 80:
        print("No good match found")
        return []

    anime_index = new_anime[new_anime['English Name'] == best_match[0]].index[0]
    print(f"Anime index: {anime_index}")

    distances, indices = nn_model.kneighbors(tfidf_matrix[anime_index], n_neighbors=top_n+1)

    recommendations = []
    for idx in indices[0]:
        anime_row = new_anime.iloc[idx]
        if anime_row['English Name'] != 'Unknown':
            recommendations.append({
                'English Name': anime_row['English Name'],
                'Image source': anime_row['Image source']
            })

    print(f"Final recommendations: {recommendations}")
    return recommendations
