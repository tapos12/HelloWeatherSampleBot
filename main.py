from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.model import Trainer, Metadata, Interpreter

import logging
import rasa_core

from rasa_core.agent import Agent
from rasa_core.domain import Domain
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy

from rasa_core.train import online
from rasa_core.utils import EndpointConfig
from rasa_core.interpreter import RegexInterpreter
from rasa_core.interpreter import RasaNLUInterpreter

from rasa_core.run import serve_application

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

import random
import warnings
import sys

'''Train and run the initial model'''
class ModelBot:
    def __init__(self):
        pass
    def train (self, data, config_file, model_dir):
        training_data = load_data(data)
        trainer = Trainer(config.load(config_file))
        trainer.train(training_data)
        model_directory = trainer.persist(model_dir, fixed_model_name = 'helloweather_model')

    def run(self):
        interpreter = Interpreter.load('./models/nlu/default/helloweather_model')
        print(interpreter.parse("How's weather in Bonn today?"))

''' Train the initial dialogue model'''
class DialogueBot:
    def __init__(self):
        logging.basicConfig(level='INFO')
        dialog_training_data_file = './data/stories.md'
        path_to_model = './models/dialogue'
        agent = Agent('weather_domain.yml', policies = [MemoizationPolicy(), KerasPolicy()])
        data = agent.load_data(dialog_training_data_file)
        agent.train(
            data,
            augmentation_factor=50,
            epochs=500,
            batch_size=10,
            validation_split=0.2)
        agent.persist(path_to_model)

'''Train dialogue online'''
class TrainDialogueOnline:
    def __init__(self):
        interpreter = RasaNLUInterpreter('./models/nlu/default/helloweather_model')
        self.run_online_trainer(interpreter)

    def run_online_trainer(self, interpreter, domain_def_file='weather_domain.yml', training_data_file='./data/stories.md'):
        action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
        agent = Agent(  domain_def_file,
            policies=[KerasPolicy(), MemoizationPolicy()],
            interpreter=interpreter,
            action_endpoint=action_endpoint)
        data = agent.load_data(training_data_file)
        agent.train( data,
            batch_size=50,
            epochs=200,
            max_training_samples=300)
        online.run_online_learning(agent)
        return agent
'''Talk to the chatbot'''
class HelloWeatherBot:
    def __init__(self):
        self.train_dialogue()
        self.run()

    def train_dialogue(self, domain_file = 'weather_domain.yml', model_path = './models/dialogue', training_data_file = './data/stories.md'):
        agent = Agent(domain_file, policies = [MemoizationPolicy(), KerasPolicy()])
        data = agent.load_data(training_data_file)  
        agent.train(
                data,
                epochs = 300,
                batch_size = 50,
                validation_split = 0.2)
        agent.persist(model_path)
        return agent

    def run(self, serve_forever=True):
        interpreter = RasaNLUInterpreter('./models/nlu/default/helloweather_model')
        action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
        agent = Agent.load('./models/dialogue', interpreter=interpreter, action_endpoint=action_endpoint)
        rasa_core.run.serve_application(agent ,channel='cmdline')
        return agent

'''Visualize the story'''
def visualize():
    agent = Agent("weather_domain.yml", policies=[MemoizationPolicy(), KerasPolicy()])
    agent.visualize("data/stories.md", output_file="graph.png", max_history=2)
if __name__ == '__main__':
    flow_type=sys.argv[1]
    #warnings.filterwarnings("ignore")
    if flow_type=='--train_model':
        ModelBot().train('./data/training_data.json', './config/config.json', './models/nlu')
        #ModelBot().run()
    elif flow_type=='--train_dialogue_init':
        DialogueBot()
    elif flow_type=='--train_dialogue_online':
        TrainDialogueOnline()
    elif flow_type=='--test':
        HelloWeatherBot()
    elif flow_type=='--visualize':
        visualize()