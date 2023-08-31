from django.shortcuts import render
from django.views import View
import pickle
import pandas as pd
# Create your views here.
class recommend(View):
    def get(self, request):
        movies_list = pickle.load(open('movietags.pkl','rb'))
        movies = pd.DataFrame(movies_list)
        return render(request, 'recommend.html' , {'data':list(movies['title'])})
    def post(self, request):
        if request.method == 'POST':
            title = request.POST.get('title')
            movies_list = pickle.load(open('movietags.pkl','rb'))
            similarity = pickle.load(open('similarity.pkl','rb'))
            movies = pd.DataFrame(movies_list)
            try:
                movie_index = movies[movies['title'] == title].index[0]
                distances = similarity[movie_index]
                movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
                recommended = []
                for i in movies_list:
                    recommended.append(movies['title'][i[0]])
                return render(request, 'recommend.html', {'rmovies':recommended,'data':list(movies['title'])})
            except:
                recommended = ['This movie is not in our database']
                return render(request, 'recommend.html', {'rmovies':recommended})