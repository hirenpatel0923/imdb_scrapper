from imdb.imdb_movie.imdb_movie import ImdbMovie

title = 'tt0082971'

flags = {'Directed': False,
                              'Writing': True,
                              'Cast': True,
                              'Produced': False,
                              'Music': False,
                              'Cinematography': False,
                              'Film': False,
                              'Art': False,
                              'Makeup': False,
                              'Production': False,
                              'Sound': False,
                              'Camera': False,
                              }

imdb_title = ImdbMovie(title=title, credit_flags=flags)


                    
print(imdb_title.title + ',' +
        imdb_title.title_name + ',' +
        str(imdb_title.ratings) + ',')

for director in imdb_title.director:
    print(director + ' ')
print(',')

for genre in imdb_title.genres:
    print(genre + ' ')
print(',')

for cast in imdb_title.get_cast_list():
    print(cast + ' ')
print(',')
