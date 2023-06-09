# Depreciated. Left in for demonstration purposes.
# Dependent on:  
#       A modified version of ChatterBot
#       The standard Chatterbot corpus
#       Spacy
#       An older version of Python 3 (max 3.6.0)
# It technically works, but meets few non-fuctional requirements. 
# The most important one, accuracy, will never be reached, due to poor documentation of database integration and search.
# In order to train on Uni.lu data, it would need to be fed conversational examples. 
# As a proof of concept, such a training file is provided, but it is too limited to be useful.
# To expand this file, to reach our accuracy target is not feasable.

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

import sys
import os
import socket
import threading

# Configure the server socket
HOST = "127.0.0.1"    # Default loopback adress
PORT = 10815
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.settimeout(1.0)
serverSocket.bind((HOST, PORT))

# Create a new chat bot and train it
binfoInfoBot = ChatBot(
    "Bot",
    logic_adapters=[
        "chatterbot.logic.MathematicalEvaluation",
        {
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "I am sorry, but I do not understand.",
            "maximum_similarity_threshold": 0.10
        }
        ]
    )

languageTrainer = ChatterBotCorpusTrainer(binfoInfoBot)
languageTrainer.train("chatterbot.corpus.english")
uniData = open(os.path.join(os.path.dirname(__file__),"..","Binfo Source File","UniLu.txt"), "r").readlines()
uniTrainer = ListTrainer(binfoInfoBot)
uniTrainer.train(uniData)

# Generate a response from the chatbot
def answer(query):
     return f"{binfoInfoBot.get_response(query)}"

# Define user interaction
def handleClient(clientSocket, clientAddress):
    connectionAccepted.set()
    print(f"{clientAddress} connected.")
    while True:
        userInput = clientSocket.recv(1024).decode()

        if not userInput:
            print(f"{clientAddress} disconnected.")
            clientSocket.close()
            break

        response = answer(userInput)
        clientSocket.send(response.encode())

# Start server
serverSocket.listen()
connectionAccepted = threading.Event()
print("BINFO Info Bot ready. Awaiting connections.")
while True:
    try:
        clientSocket, clientAddress = serverSocket.accept()
        clientThread = threading.Thread(target=handleClient, args=(clientSocket, clientAddress), daemon=True)
        clientThread.start()
    except  socket.timeout: {}    
    except KeyboardInterrupt:
        sys.exit()

# py ./code/client.py