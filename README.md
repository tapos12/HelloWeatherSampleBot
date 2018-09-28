# HelloWeather Simple Chatbot

## Introduction
In this simple chatbot demo program, I have used RASA conversational AI solution.

The use case for the bot is, it will respond question based on weather of some specific location. Here I used 5 different intents of the dialogue model based on the intents different stories are performed.

#### Intents
##### -	 greet (Hey / Hello)
##### - goodbye (Bye / See ya)
##### - ask_weather (What's the weather today?)
##### - ask_ weather_location (How's weather in Stuttgart? / In Paris)
##### - ask_temperature (What is current temperature in Berlin?)

Based on this intent, for simplicity, I just used some random values and variety weather condition in random as a repond of the bot.

An overview of the story is given below-

## Installing + Running

My version of building the bot is running on Mac OSX with Python 3.6.6, Rasa core 0.11.7 and Rasa NLU 0.13.4.

To build the NLU-

``` pip install rasa_nlu ```

To install necessary other libraries in it-

``` pip install -r requirements.txt ```
``` python -m spacy download en ```


For adding necessary training data for general model, I used the extensive tool provided by rasa which is accessible in command-

``` rasa-nlu-trainer ```

To train this model-

``` python main.py --train_model ```

A dialogue model with intent and action has been created in weather_domain.yml . And based on the intents and actions, several stories has been created on data/stories.md . To train the initial dialogue model, first start the custom action server by running

``` python -m rasa_core_sdk.endpoint --actions actions ```

And then in a new terminal, rasa core model can be run by follows- 

``` python main.py --train_dialogue_init ```

To create some realtime data into stories, RASA provides an online training approach. To train the dialogue online-

``` python main.py --train_dialogue_online ```

To visualize the overall stories workflow-

```python main.py --visualize```

To test the system (Actual chat with the chatbot) -

``` python main.py --test ```

A demo overview of the test result-

Use case #1

``` 
User: Hello
Bot: Hello, What can I do for you?
User: What's the weather today?
Bot: Which city specifically?
User: In Manchester
Bot:  It is sunny in manchester at this moment. The temperature is 5 degree and the wind speed is 83 mph. 
User: Ok, thanks. Bye
Bot: See you soon
```

Use case #2

```
User: Hello there
Bot: Hello!
User: How's weather today in Moscow?
Bot:  It is sunny in moscow at this moment. The temperature is 23 degree and the wind speed is 225 mph. 
User: And what about temperature in St. petersburg?
Bot:  The temperature in st is now 0 degree currently 
User: thanks, cya
Bot: See you soon
