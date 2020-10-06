#########################################
##### Name: Chang Ge                #####
##### Uniqname: 01549121            #####
#########################################
import json
import webbrowser
import requests

class Media:

    def __init__(self, title="No Title", author="No Author", release_year='No Release Year', url='No URL', json=None):
        if json == None:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url
        else:
            try:
                self.title = json['trackCensoredName']
            except:
                self.title = json['collectionCensoredName']
            self.author = json['artistName']
            self.release_year = json['releaseDate'][0:4]
            try:
                self.url = json['trackViewUrl']
            except:
                self.url = json['collectionViewUrl']
    
    def info(self):
        return self.title + ' by ' + self.author + ' (' + str(self.release_year) + ')'
    
    def length(self):
        return 0

class Song(Media):
    def __init__(self, title='No Title', author="No Author", release_year='No Release Year', url='No URL', album='No Album', genre='No Genre', track_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json == None:
            self.album = album
            self.genre = genre
            self.track_length = track_length
        else:
            self.title = json['trackCensoredName']
            self.album = json['collectionCensoredName']
            self.genre = json['primaryGenreName']
            self.track_length = json['trackTimeMillis']

    def info(self):
        return self.title + ' by ' + self.author + ' (' + str(self.release_year) + ') [' + self.genre + "]"

    def length(self):
        return int(int(self.track_length)/1000)

class Movie(Media):
    def __init__(self, title='No Title', author="No Author", release_year='No Release Year', url='No URL', rating='No Rating',movie_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json == None:
            self.rating = rating
            self.movie_length = movie_length
        else:
            self.rating = json['contentAdvisoryRating']
            self.movie_length = json['trackTimeMillis']

    def info(self):
        return self.title + ' by ' + self.author + ' (' + str(self.release_year) + ') [' + self.rating + "]"
    
    def length(self):
        return int(int(self.movie_length)/60000)


def get_api_resource(search_word):
    """
    Parameters:
        params (dict): optional dictionary of querystring arguments. The default value is None.
    
    Returns:
        dict: dictionary representation of the decoded JSON.
    """
    itunes = 'https://itunes.apple.com/search'
    params = {}
    params['term'] = search_word
    response = requests.get(itunes, params)
    if response.status_code == 200:
        py_dict = response.json()
        return py_dict['results']
    else:
        print('Fail, status code: ' + response.status_code)

def create_Media(media_dict):
    list = []
    try:
        for i in media_dict:
            if i['kind'] == 'song':
                list.append(Song(json=i))
            elif i['kind'] == 'feature-movie':
                list.append(Movie(json=i))
            else:
                list.append(Media(json=i))
    except:
        list.append(Media(json=i))
    return list

def print_Media(media_list):
    head = ''
    if len(media_list) != 0:
        for i, var in enumerate(media_list):
            if str(var.__class__.__name__) != head:
                print()
                if str(var.__class__.__name__) == 'Song':
                    print('SONGS')
                elif str(var.__class__.__name__) == 'Movie':
                    if head == '':
                        print('SONGS\nNo songs found.\n')
                    print('MOVIES')
                else:
                    if head == '':
                        print('SONGS\nNo songs found.\n \nMOVIES\nNo movies found.\n')
                    print('OTHER MEDIA')
                head = str(var.__class__.__name__)

            print('{} {}'.format(i+1,var.info()))
        if head != 'Media':
            if head == 'Song':
                print('MOVIES\nNo movies found.\n')
                print('OTHER MEDIA\nNo other media found.\n')
            elif head == 'Movie':
                print('OTHER MEDIA\nNo other media found.\n')
    else:
        print('No media found.')
        
def view_detail(num):
    url = list[int(num)-1].url
    print('Launching\n' + url + '\nin web browser...')
    webbrowser.open_new_tab(url)                


# Other classes, functions, etc. should go here


if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    list = []
    search_word = input('What would you like to search? Enter a key word to search or exit to quit: ')
    while search_word.lower() != 'exit':
        if search_word.isnumeric() is False or len(list)==0:
            response = get_api_resource(search_word)
            list = create_Media(response)
            print_Media(list)
        else:
            view_detail(search_word)
        search_word = input('Enter the index number to view detail, or new keyword for new search, or exit to quit: ')

    print('Thanks for using the service!')