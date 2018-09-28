from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

import random

'''Get "action_weather" data'''
class ActionWeather(Action):
    def name(self):
        return 'action_weather'

    def run(self, dispatcher, tracker, domain):
        loc = tracker.get_slot('location')
        weather_cond = ['sunny', 'rainy', 'snowy', 'cloudy']
        temp = list(range(0,35))
        wind = list(range(50,250))
        response = """ It is {} in {} at this moment. The temperature is {} degree and the wind speed is {} mph. """. format( random.choice(weather_cond), loc, random.choice(temp), random.choice(wind))
        dispatcher.utter_message(response)
        return [SlotSet('location',loc)]

'''Get "action_temp" data'''
class ActionTemperature(Action):
    def name(self):
        return 'action_temp'

    def run(self, dispatcher, tracker, domain):
        loc = tracker.get_slot('location')
        temp = list(range(0,35))
        response = """ The temperature in {} is now {} degree currently """. format( loc, random.choice(temp))
        dispatcher.utter_message(response)
        return [SlotSet('location',loc)]