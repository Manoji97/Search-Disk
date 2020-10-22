from flask import Flask, render_template, request
import os

app = Flask(__name__)


def get_all_files():
    lookup_dict = {}
    dir_list = ['MOVIES', 'COURSES', 'OS', 'GAMES', 'DUMMY', 'APPLICATIONS', 'SERIES']
    for directory in os.listdir('../'):
        if directory in dir_list:
            lookup_dict[directory] = recursion_helper(f'../{directory}', [])
    return lookup_dict

def recursion_helper(path, files_lst = []):
    directory_lst = os.listdir(path)
    for directory in directory_lst:
        if directory.isupper():
            files_lst += recursion_helper(f'{path}/{directory}', [])
        else:
            files_lst.append({'name': directory, 'location': path})
    return files_lst

        
LookUp_Files = get_all_files()
print(LookUp_Files)

def search_lookup(search_key):
    searched_lookup = {}
    for folder in LookUp_Files:
        searched_lookup[folder] = []
        for file in LookUp_Files[folder]:
            if search_key in file['name'].lower(): searched_lookup[folder].append(file)
    return searched_lookup


@app.route('/')
def search_file():
    """
    docstring
    """
    search_key = request.args.get('search_key')
    if not search_key:
        search_lst = LookUp_Files
    else:
        search_lst = search_lookup(search_key.lower())
    return render_template('index.html', res_list = search_lst)

@app.errorhandler(404)
def errorhandler(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run()