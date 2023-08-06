import numpy as np
import wikipedia
from transformers import DistilBertTokenizer, DistilBertModel #BertTokenizer, BertModel
import torch
import json
import fire
from scipy.spatial import distance
from pkg_resources import resource_stream
import transformers
transformers.logging.set_verbosity_error()

def get_text(movie, year):
    try:
        text = wikipedia.WikipediaPage(title = movie).summary
    except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError) as e:
        try:
            new_movie = movie + " (film)"
            text = wikipedia.WikipediaPage(title = new_movie).summary
        except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError) as e:
            try:
                new_movie = movie + " (" + str(year) + " " + "film)"
                text = wikipedia.WikipediaPage(title = new_movie).summary
            except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError) as e:
                text = ""
    text = text.replace('\n','').replace("\'","")
    if text=="":
        print("Could not find the summary, are you sure this is the right title on Wikipedia ?")
    return text

def save_movie_summaries():
    df = pd.read_csv('sight_sound_rank.tsv', sep='\t')
    movies = df['movie'].to_numpy()
    years = df['year'].to_numpy()
    movies[9] = "Breathless (1960 film)"
    movies[12] = "The Mirror (1913 film)"
    movies[36] = "Psycho (1960 film)"
    movies[43] = "Fanny and Alexander"
    movies[44] = "The General (1926 film)"
    movies[46] = "Modern Times (film)"
    movies[47] = "Gertrud (film)"
    movies[0] = "Vertigo (film)"
    movies[50] = "Jeanne Dielman, 23 quai du Commerce, 1080 Bruxelles"
    movies[54] = "The Night of the Hunter (film)"
    movies[61] = "Histoire(s) du cinéma"
    movies[63] = "Blue Velvet (film)"

    movie_summaries = dict()
    for i in range(len(movies)):
        movie, year = movies[i], years[i]
        text = get_text(movie, year)
        if text != "":
            movie_summaries[movie] = text 
    
    print("number of movies missing = ", no_summaries)
    json = json.dumps(movie_summaries)
    f = open("movie_summaries.json","w")
    f.write(json)
    f.close()
    
def save_movie_vectors(tokenizer, model):
    
    def get_vector(movie, model):
        model.eval()
        text = movie_summaries[movie]
        inputs = tokenizer(text, return_tensors="pt", max_length=500, truncation=True)
        inputs.requires_grad=False
        last_hidden_states = model(**inputs).last_hidden_state[0][-1].detach().numpy()
        return last_hidden_states

    movie_vectors = dict()
    for i, movie in enumerate(movie_summaries.keys()):  
        last_hidden_states = get_vector(movie, model)
        movie_vectors[movie] = last_hidden_states.tolist()
        gc.collect()

    json = json.dumps(movie_vectors)
    f = open("movie_vectors.json","w")
    f.write(json)
    f.close()
    

def get_movie_recommendations(
    movie_name="The Godfather Part III", 
    movie_year=1990
    ):
    json_string = resource_stream(__name__, 'data/movie_summaries.json').read().decode()
    movie_summaries = json.loads(json_string)
    json_string = resource_stream(__name__, 'data/movie_vectors.json').read().decode()
    movie_vectors = json.loads(json_string)
    
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = DistilBertModel.from_pretrained('distilbert-base-uncased')
    new_text = get_text(movie_name, movie_year)
    inputs = tokenizer(new_text, return_tensors="pt", max_length=300, truncation=True)
    new_vector = model(**inputs).last_hidden_state[0][-1].detach().numpy()

    all_scores = np.round(np.array([distance.cosine(new_vector, movie_vectors[movie]) \
                           for movie in movie_vectors]), 3)

    num_scores = 15
    top_scores = np.argsort(all_scores)[:num_scores]
    print("Movies, Scores (from 0 to 1)")
    for movie, score in zip([list(movie_vectors.keys())[elem] for elem in top_scores], list(1-all_scores[top_scores])):
        print(movie, score)
        
def main():
    fire.Fire(get_movie_recommendations)
    
if __name__ == "__main__":
    fire.Fire(get_movie_recommendations)