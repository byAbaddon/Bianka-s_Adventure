import collections.abc
collections.MutableMapping = collections.abc.MutableMapping
collections.Mapping = collections.abc.Mapping
collections.Iterable = collections.abc.Iterable
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable

# not change import requests position!
import requests

'''
===============================================================================================
                                 *** Don't be a bastard ***
===============================================================================================
'''

url = 'https://gamebiankasadventureuserscore-default-rtdb.europe-west1.firebasedatabase.app/'
response = requests.get(url + '.json')


# ------------------------------------------- GET
def get():
    if response.status_code == 200:
        print("Successful connection...")
        data = response.json()
        # print(data)
        return data
    elif response.status_code == 404:
        print("Unable to reach URL.")
    else:
        print("Unable to connect API or retrieve data.")


# ------------------------------------------ POST
def post(name_player, current_score):
    current_player = {name_player: current_score}
    add_post = requests.post(url + 'score.json', json=current_player)
    print(add_post.text)


# ----------------------------------------- DELETE
def delete(data_key):
    x = requests.delete(url + 'score/' + data_key + '/.json')
    return x.status_code
# ----------------------------------------- work with response data

# post('Lina' , 3000)


def ranking_manipulator():
    dict_of_players = {}
    try:
        for res_data in get().values():
            for key, player in res_data.items():
                if len(dict_of_players) < 10:  # allowed only 10 players in dict
                    name = list(player.keys())[0]
                    score = list(player.values())[0]
                    dict_of_players[name] = score
                else:  # delete more form 10 players
                    delete(key)
                    print('Delete success')
        sorted_list_of_players = sorted(dict_of_players.items(), key=lambda x: -x[1])
        return sorted_list_of_players
        # for k, v in sorted_list_of_players:
        #     print(k, v)
    except:
        print('Requests operation failed')
        return []


# ranking_manipulator()