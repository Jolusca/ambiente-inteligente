import threading
import socket
import dispositivo_pb2 as dispositivo_pb2
import sys

raw_input = input  # Python 3
username = 'som'


''' Pelo menos um dos equipamentos deve atuar como um sensor contínuo, que envia 
    a cada ciclo de X segundos um valor para o Gateway (e.g., um sensor de
    temperatura). Essa funcionalidade deve ser implementada com socket do tipo
    UDP. '''

def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 7776))
        host, port = client.getsockname()
        print(f'{host, port}')
        print(f'{port}')
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')
    
    # Add an address.
    PromptForDispositivo(aparelhos_book.aparelhos, username)
    apresentar(client)
    print('\nConectado')

    # instanciar classes

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    thread1.start()
    thread2.start()
    
def receiveMessages(client):
    while True:
        try:
            #aparelhos_book = dispositivo_pb2.AparelhosBook()
            msg = client.recv(2048)
            temp = msg.decode()
            if temp == 'Chamada':
                resposta = (f'<{username}> {client.getsockname()}')
                print(resposta)
                data_string = str.encode(resposta)
                sendAnswer(client, data_string)
                print('enviou')
            else:
                aparelhos_book.ParseFromString(msg)
                print(aparelhos_book.ListFields())
                sendMessages(client, msg)
                print('enviou')
                
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            continue


def sendAnswer(client, msg):
    for i in range(1,3):
        try:

            #msg = aparelhos_book.SerializeToString()
            #aparelhos_book.aparelhos.name = "jl"
            client.send(msg)
            #picles = pickle.dumps(f'<{username}> {msg}')
       
        except:
            continue
        
def sendMessages(client, msg):

        msg = aparelhos_book.SerializeToString()
        #aparelhos_book.aparelhos.name = "jl"
        client.send(msg)
        #picles = pickle.dumps(f'<{username}> {msg}')

        
def apresentar(client):
    try:
        msg = aparelhos_book.SerializeToString()
        client.send(msg)
    except:
            return

# This function fills in a Person message based on user input.
def PromptForDispositivo(aparelho, username):
  aparelho.name = username
  aparelho.on = 'D E S L I G A D O'
  aparelho.volume = '0'
  
# Main procedure:  Reads the entire address book from a file,
#   adds one person based on user input, then writes it back out to the same
#   file.

aparelhos_book = dispositivo_pb2.AparelhosBook()
        
main()