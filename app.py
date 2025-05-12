from flask import Flask, request, render_template, send_from_directory, jsonify
import pickle
import os
import pandas as pd
from fuzzywuzzy import process
from anime_recommendation import load_models, get_recommendations  # Import your functions
import kagglehub

app = Flask(__name__)

# Load data and models when the app starts (not inside the route)
new_anime, nn_model, TfidfVectorizer, tfidf_matrix = load_models()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/anime_data.json')
def serve_anime_data():
    return send_from_directory('static', 'anime_data.json')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = request.get_json()

            # Extract the anime name from the parsed JSON
            anime_name = data.get('anime_name', '').strip().lower()

            if not anime_name:
                return jsonify({'error': 'Please enter an anime name.'}), 400

            # Get recommendations based on anime_name
            recommendations = get_recommendations(anime_name, top_n=20)
            print("Recommendations:", recommendations)  # Debugging line

            if not recommendations:
                return jsonify({'error': 'Anime not found. Please try another name.'}), 404

            # Return recommendations in JSON format
            return jsonify({'recommendations': recommendations})

        except Exception as e:
            return jsonify({'error': f"An error occurred: {str(e)}"}), 500

    return render_template('search.html')

@app.route('/Genre.html')
def genre():
    return render_template('Genre.html')

@app.route('/anime.html')
def anime():
    anime_name = request.args.get('anime_name', 'Unknown Anime')
    return render_template('anime.html', anime_name=anime_name)

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/feedback.html')
def feedback():
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True)
