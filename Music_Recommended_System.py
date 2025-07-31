import pandas as pd
import numpy as np
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle


data= pd.read_csv(r"C:\Users\hp\.vscode\Project_Machine-Learning\Project-14\spotify_millsongdata.csv")
data.drop(columns=["link"],inplace=True)
# data = data.sample(5000).reset_index(drop=True)
data  = data.iloc[:6000]
print(data["song"])



data["text"] = data["text"].str.replace('\n', '').str.replace('\r', '').str.replace('\t', '').str.replace('  ', ' ')
data["tag"] = data["artist"] +" "+ data["text"]
data.drop(columns=["text"],inplace=True)


ps = PorterStemmer()
def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

data["tag"] = data["tag"].apply(stem)

cv = TfidfVectorizer(stop_words="english",analyzer="word")
vector = cv.fit_transform(data["tag"]).toarray()
similarity = cosine_similarity(vector)

def recommend(song):
    index = data[data["song"]==song].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    for i in distances[1:6]:
       print(data.iloc[i[0]].song)


recommend("Love For Tender")

pickle.dump(data,open("Music_recommender.pkl","wb"))
pickle.dump(similarity,open("similarity.pkl","wb"))



