import random
import requests
import string


class DefaultTask:
    def __init__(self, data):
        self.title = data['title']
        self.id_labels = TrelloAPI.labels[data['type']]
        self.error = ''


class Bug(DefaultTask):
    def __init__(self, data):
        super().__init__(data)
        random_word = ''.join((random.choice(string.ascii_uppercase) for x in range(5)))
        random_int = random.randint(0, 100)
        self.title = f'bug-{random_word}-{random_int}'


class Issue(DefaultTask):
    pass


class Task(DefaultTask):
    def __init__(self, data):
        super().__init__(data)
        if TrelloAPI.labels.get(data["category"]):
            self.id_labels = f'{TrelloAPI.labels[data["type"]]},{TrelloAPI.labels[data["category"].lower()]}'
        else:
            self.error = {'Category Error': f'The category does not exist. Categories available: {"-".join([x for x in TrelloAPI.labels_colors if x not in ["bug", "issue", "task"]])}'}


class TrelloAPI:
    BASE_URL = 'https://api.trello.com/1/'
    HEADERS = {"Accept": "application/json"}
    TOKEN = '9881d6adbe1cbf182eca5a8c00935e32299447b3e73e296c1d89891bd19b8304'   # replace with the TOKEN of the account
    KEY = 'c7cd5b4d0ef40b52e6b8e3f1b9b6df3e'                                     # replace with the KEY of the account
    BOARD_NAME = 'spaceX'                                                        # replace with the current BOARD_NAME of the account
    id_board = ''
    id_list = ''
    labels = {}
    labels_colors = {
            'task': 'green',
            'issue': 'orange',
            'bug': 'red',
            'maintenance': 'yellow',
            'test': 'purple',
            'research': 'blue'
        }

    def get_board_id():
        url = f'{TrelloAPI.BASE_URL}members/me/boards?fields=name,url&key={TrelloAPI.KEY}&token={TrelloAPI.TOKEN}'
        response = requests.get(url)
        boards = response.json()
        for board in boards:
            if board.get('name') == TrelloAPI.BOARD_NAME:
                TrelloAPI.id_board = board.get('id')
                break

    def get_labels():
        """
        method to get the ids of the labels and save them into a dict variable self.labels and create them 
        if they do not exists
        """
        url = f'{TrelloAPI.BASE_URL}labels'
        for label, color in TrelloAPI.labels_colors.items():
            query = {
                'key': TrelloAPI.KEY,
                'token': TrelloAPI.TOKEN,
                'idBoard': TrelloAPI.id_board,
                'name': label,
                'color': color
            }
            response = requests.post(url, params=query)
            TrelloAPI.labels[label] = response.json()['id']

    def get_list():
        """
        get the id of the list To Do and save it into a string variable self.id_list, this method creates 
        the list if it does not exists
        """
        url = f'{TrelloAPI.BASE_URL}boards/{TrelloAPI.id_board}/lists'
        query = {
            'key': TrelloAPI.KEY,
            'token': TrelloAPI.TOKEN
        }
        response = requests.get(url, headers=TrelloAPI.HEADERS, params=query)
        lists = response.json()
        for list in lists:
            if list['name'] == 'To Do':
                TrelloAPI.id_list = list['id']
                return
        list_url = "https://api.trello.com/1/lists"
        query = {
            'key': TrelloAPI.KEY,
            'token': TrelloAPI.TOKEN,
            'idBoard': TrelloAPI.id_board,
            'name': 'To Do'
        }
        response = requests.post(list_url, params=query)
        TrelloAPI.id_list = response.json().get('id')

    def create_card(data):
        """
        Method to create a card with the data input from the serializer
        """
        card = eval(data['type'].capitalize())(data)
        if not card.error:
            url = f'{TrelloAPI.BASE_URL}cards'
            query = {
                'key': TrelloAPI.KEY,
                'token': TrelloAPI.TOKEN,
                'idList': TrelloAPI.id_list,
                'name': card.title,
                'idLabels': card.id_labels,
                'desc': data['description']
            }
            response = requests.post(url, headers=TrelloAPI.HEADERS, params=query)
            if data['type'] == 'bug':
                TrelloAPI._assign_card(response.json()['id'])
            return response.json()
        else:
            return card.error

    def _assign_card(id_card):
        """
        Private method to assign a card to a member of the board
        """
        id_member = TrelloAPI._get_random_member()
        url = f'{TrelloAPI.BASE_URL}cards/{id_card}/idMembers'
        query = {
            'key': TrelloAPI.KEY,
            'token': TrelloAPI.TOKEN,
            'value': id_member
        }
        requests.post(url, params=query)

    def _get_random_member():
        """
        Private method to get and return a random member of the board
        """
        url = f'{TrelloAPI.BASE_URL}boards/{TrelloAPI.id_board}/members'
        query = {
            'key': TrelloAPI.KEY,
            'token': TrelloAPI.TOKEN,
        }
        response = requests.get(url, headers=TrelloAPI.HEADERS, params=query)
        member = random.choice(response.json())
        return member['id']


def card_factory(data):
    """
    Factory method to create a card in Trello with the data input from the serializer
    """
    if not TrelloAPI.id_board:
        TrelloAPI.get_board_id()
    if not TrelloAPI.labels:
        TrelloAPI.get_labels()
    if not TrelloAPI    .id_list:
        TrelloAPI.get_list()
    response = TrelloAPI.create_card(data)
    return response