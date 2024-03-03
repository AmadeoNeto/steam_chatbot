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
import utils
import sqlite3
from transformers import pipeline

path_to_game_info_db = r"steam_base.db"

# Load the pre-trained question answering pipeline
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad", tokenizer="distilbert-base-uncased")

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
            # publisher = tracker.get_slot('publisher')
            developer = tracker.get_slot('developer')
            release_date = tracker.get_slot('release_date')
            game_tag = tracker.get_slot('game_tag')

            print('\n::SLOTS::')
            print('platform', platform)
            print('genre', genre)
            print('categories', categories)
            # print('publisher', publisher)
            print('developer', developer)
            print('release_date', release_date)
            print('game_tag', game_tag)
            print()

            query = utils.query_builder(game_tag   = game_tag,
                    platforms     = platform,
                    genres        = genre,
                    categories   = categories,
                    developer    = developer,
                    release_date = release_date)

            cur = conn.cursor() 

            res_query = cur.execute(query)

            data_row = res_query.fetchone()


            return_slots = [SlotSet('platform', None),
                            SlotSet('genre', None),
                            SlotSet('category', None),
                            SlotSet('developer', None),
                            SlotSet('release_date', None),
                            SlotSet('game_tag', None)]

            print('DB response: ',data_row)

            if data_row:
                dispatcher.utter_message(f'You should try {data_row[1]}, what do you think?')

                conn.close()
                return [return_slots]
            else:
                dispatcher.utter_message(template="uteer_recom_not_found")

                conn.close()
                return [return_slots]


class RequestInfo(Action):

    def name(self) -> Text:
        return "action_request_info"
    
    def run(self,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            conn = sqlite3.connect(path_to_game_info_db)

            game_title = tracker.get_slot('game_title')

            print('\n::SLOTS::')
            print('game title', game_title)
    
            # Define question and context
            question = tracker.latest_message.get('text')
            context = utils.generate_qa_context(game_title, conn)

            print('Question: ', question)
            print('Context: ',context)
    
            if game_title is None or context == '':
                dispatcher.utter_message(text = "Sorry, I do not get the game name!")
                conn.close()
                return []

            # Perform question answering
            answer_dsbert = qa_pipeline(question=question, context=context)
            print("\nAnswer:", answer_dsbert["answer"])
            print("\Confidence:", answer_dsbert["score"])

            if context != "":
                answer = answer_dsbert['answer']
                answer = ", ".join(answer.split(';')).title()
                confidence = answer_dsbert['score']

                response = f'{answer}. '
                if confidence < 0.25:
                    response += "But I'm not sure."
                elif confidence > 0.80:
                    response += "For sure!"

                dispatcher.utter_message(text = response)

                conn.close()
                return []
            else:
                dispatcher.utter_message(template="uteer_recom_not_found")
                conn.close()
                return []
            