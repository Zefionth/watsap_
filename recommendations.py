from openai_api import get_names
from kinopoisk_api import get_info_movies
from shikimoriapi import get_info_anime

def get_recommendations(query: str, category: str) -> list:

    recommendations = []

    names = get_names(query, category).values()
    if names:
        if category == 'movies':
            for name in names:
                if name == None: continue
                info = get_info_movies(name)
                recommendations.append(info)
        else:
            for name in names:
                if name == None: continue
                info = get_info_anime(name)
                recommendations.append(info)

    return recommendations