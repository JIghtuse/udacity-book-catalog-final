# List is based on Wikipedia articles:
# https://en.wikipedia.org/wiki/List_of_writing_genres
# https://en.wikipedia.org/wiki/Comedy
# https://en.wikipedia.org/wiki/Literary_fiction
# https://en.wikipedia.org/wiki/Drama
# https://en.wikipedia.org/wiki/Fantasy

genres = [{'name': "comedy",
           'description': "Books intended to be humorous or amusing by inducing laughter"},
          {'name': "classic",
           'description': "Fiction that has become part of an accepted literary canon, widely taught in schools"},
          {'name': "drama",
           'description': 'Specific mode of fiction represented in performance.[1] The term comes from a Greek word meaning "action" (Classical Greek: δρᾶμα, drama), which is derived from "to do" (Classical Greek: δράω, drao)'},
          {'name': "fantasy",
           'description': "Fiction genre that uses magic or other supernatural elements as a main plot element, theme, or setting. Many works within the genre take place in imaginary worlds where magic and magical creatures are common."
          }]

recent_books = [
    {
        'title': "Game of Thrones",
        'cover_url': "https://upload.wikimedia.org/wikipedia/en/9/93/AGameOfThrones.jpg",
        'author': "George Martin",
        'description': "Long ago, in a time forgotten, a preternatural event threw the seasons out of balance. In a land where summers can last decades and winters a lifetime, trouble is brewing. The cold is returning, and in the frozen wastes to the north of Winterfell, sinister forces are massing beyond the kingdom’s protective Wall. To the south, the king’s powers are failing—his most trusted adviser dead under mysterious circumstances and his enemies emerging from the shadows of the throne. At the center of the conflict lie the Starks of Winterfell, a family as harsh and unyielding as the frozen land they were born to. Now Lord Eddard Stark is reluctantly summoned to serve as the king’s new Hand, an appointment that threatens to sunder not only his family but the kingdom itself.",
        'year': 1996,
        'buy_url': 'https://www.amazon.com/Game-Thrones-Song-Ice-Fire/dp/0553103547/ref=sr_1_1?s=books&ie=UTF8&qid=1479576348&sr=1-1&keywords=game++of+thrones+1996',
        'genre': {'name': 'fantasy'}
    },
    {
        'title': "Lord of rings",
        'genre': {'name': 'fantasy'}
    },
    {
        'title': "War and Peace",
        'genre': {'name': 'classic'}
    },
]
