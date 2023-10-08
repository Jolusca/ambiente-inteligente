import threading
import socket
import dispositivo_pb2 as dispositivo_pb2
import sys

raw_input = input  # Python 3



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
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')

    username = input('Usuário> ')
    
    # Add an address.
    PromptForDispositivo(aparelhos_book.aparelhos, username)
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
            # Read the existing address book.
            print(aparelhos_book.ListFields())
            msgs = str(aparelhos_book.ParseFromString(msg))
            #msg = pickle.loads(msg)
            print(msgs+'\n')
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break


def sendMessages(client, username):
    while True:
        try:
            input("digite algo")
            #aparelhos_book = dispositivo_pb2.AparelhosBook()
            # Add an address.
            # PromptForDispositivo(aparelhos_book.aparelhos.write())
            # Write the new address book back to disk.

            msg = aparelhos_book.SerializeToString()
            #aparelhos_book.aparelhos.name = "jl"
            print(aparelhos_book.aparelhos.name)
            

            #picles = pickle.dumps(f'<{username}> {msg}')
            
            client.send(msg)
        except:
            return

# This function fills in a Person message based on user input.
def PromptForDispositivo(aparelho, username):
  aparelho.name = username
  aparelho.on = bool(1)
  aparelho.volume = int(7)
  
# Main procedure:  Reads the entire address book from a file,
#   adds one person based on user input, then writes it back out to the same
#   file.

aparelhos_book = dispositivo_pb2.AparelhosBook()


main()