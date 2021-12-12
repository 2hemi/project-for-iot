import time
import socket
import ast
import json
import pickle
from flask import request
from flask import Flask
from flask_restful import Resource,Api,reqparse


HOST = '192.168.1.121'
PORT = 8888
def get_socket():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)
    string = data.decode('utf-8')   
    #return ast.literal_eval(string)
    print( string) 

    return string

def toJson(tab):

    string = {"temperature":str(tab[0]),"humidity":str(tab[1]),"rain":str(tab[2])}
    

    #return ast.literal_eval(string)
    return string

def prediction(temp,humd):
    
    file = "model2.model"
    #pickle.dump(logReg,open(file,'wb'))

    loaded_model = pickle.load(open(file, 'rb'))
    result = loaded_model.predict([[temp,humd]])
    
    return result
    

class Weather(Resource):
    def get(self):  
        data = get_socket()

        if data == 'error':
            return {'value':'ERROR'}
        else: 
            #data = "50/10/cloud"
            tab = data.split('/')
            x = (float(tab[0])*9/5)+32
            pred = prediction(x, tab[1])
            if 'Rain' in pred[0]:
                tab[2] = 'rain'
            elif 'Clear' in pred[0]:
                tab[2] = 'clear'
            else :
                tab[2] = 'cloudy'

            return toJson(tab)


        #return data

#print(a)
app = Flask(__name__)
api = Api(app)
api.add_resource(Weather,'/weather')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
