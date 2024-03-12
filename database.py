from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb://localhost:27017"
rainbow_order = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]


class MongoDb:
    def __init__(self):
        # Create a new client and connect to the server
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.collist_name = ['Tool', 'Kit', 'Transition']
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        self.mydb = self.client["BE_Exam"]
        self.collist = self.mydb.list_collection_names()
        self.users_collection = self.mydb['Users']
        self.homes_collection = self.mydb['Homes']
        self.rooms_collection = self.mydb['Rooms']
        self.lights_collection = self.mydb['Lights']
        self.lights_status_collection = self.mydb['Light_Status']

    def get_room(self, room_id: int):
        return self.rooms_collection.find_one({'ID': room_id})

    def get_light(self, light_id: int):
        light = self.lights_collection.find_one({'ID': light_id})
        return {
            'Name': light['Name'],
            'Color': light['Color'],
            'Brightness': light['Brightness']
        }

    def get_lights_in_room(self, room_id: int):
        room = self.get_room(room_id=room_id)
        lights_in_room = room['Lights']
        results = []
        for light in lights_in_room:
            results.append(self.get_light(light_id=light))
        sorted_results = sorted(results, key=lambda x: rainbow_order.index(x["Color"]))
        return sorted_results
