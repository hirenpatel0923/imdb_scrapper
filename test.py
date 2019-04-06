from imdb_title import ImdbTitle

title = 'tt0082971'


imdb_title = ImdbTitle(title=title)
                    
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
