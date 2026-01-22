from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# ---------- LOAD PICKLE FILES ----------
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Normalize titles once
movies['title'] = movies['title'].str.lower().str.strip()

# ---------- RECOMMEND FUNCTION ----------
def recommend(movie):
    movie = movie.lower().strip()

    if movie not in movies['title'].values:
        return []

    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    return [movies.iloc[i[0]].title for i in movies_list]

# ---------- ROUTES ----------
@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []
    error = None

    if request.method == 'POST':
        movie = request.form['movie']
        recommendations = recommend(movie)

        if not recommendations:
            error = "Movie not found in dataset"

    return render_template(
        'index.html',
        recommendations=recommendations,
        error=error
    )

# ---------- RUN ----------
if __name__ == '__main__':
    app.run(debug=True)
