# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import sqlite3

path_to_game_info_db = r"steam_base.db"

# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []


class RecommendGame(Action):

    def name(self) -> Text:
        return "action_recommend_game"
    
    def run(self,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            conn = sqlite3.connect(path_to_game_info_db)

            platform = tracker.get_slot('platform')
            genre = tracker.get_slot('genre')
            categories = tracker.get_slot('category')
            publisher = tracker.get_slot('publisher')
            developer = tracker.get_slot('developer')
            release_date = tracker.get_slot('release_date')
            game_tag = tracker.get_slot('game_tag')

            print('\n::SLOTS::')
            print('platform', platform)
            print('genre', genre)
            print('categories', categories)
            print('publisher', publisher)
            print('developer', developer)
            print('release_date', release_date)
            print('game_tag', game_tag)
            print()

            game_tag = game_tag[0]
            print('Used game tag:', game_tag)

            query = '''
                SELECT name, steamspy_tags FROM game_info
                WHERE steamspy_tags LIKE ? 
                AND positive_ratings = (
                    SELECT MAX(positive_ratings)
                    FROM game_info
                    WHERE steamspy_tags LIKE ?
                )
            '''

            cur = conn.cursor() 

            res_query = cur.execute(query, ('%' + game_tag + '%', '%' + game_tag + '%'))

            data_row = res_query.fetchone()

            print('DB response: ',data_row)

            if data_row:
                dispatcher.utter_message(f'You should try {data_row[0]}, what do you think?')

                conn.close()
                return [SlotSet("game_title", data_row[0])]
            else:
                dispatcher.utter_message(text="uteer_recom_not_found")

                conn.close()
                return []



