import threading
import socket
from time import sleep
import dispositivo_pb2 as dispositivo_pb2
import pickle

listaClient = [3]
listaNome = [3]
listaPort = [3]
j:bool = True
i:int = 0

def main():

    gateway = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        gateway.bind(('localhost', 7776))
        gateway.listen()
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        client, addr = gateway.accept()
        listaClient.append(client)
        print(client)

        print(addr)
        host, port = client.getpeername()
        print(port)
        
        listaPort.append(port)
        salvarNome(client)
        
        if len(listaNome) == 3:      
            thread1 = threading.Thread(target=messagesTreatment1, args=[listaClient[1]])
            thread2 = threading.Thread(target=messagesTreatment2, args=[listaClient[2]])
            thread3 = threading.Thread(target=sendMessages)
            thread1.start()
            thread2.start()
            thread3.start()

def salvarNome(client):
    try:
        msg = client.recv(2048)
        aparelhos_book.ParseFromString(msg)
        if aparelhos_book.aparelhos.name == 'lampada':
            listaNome.append(aparelhos_book.aparelhos.name)
        if aparelhos_book.aparelhos.name == 'som':
            listaNome.append(aparelhos_book.aparelhos.name)

        print('\n-----')
        for i in range(1,len(listaNome)):    
            print(listaNome[i],listaPort[i])
        print(aparelhos_book.ListFields())
        print('-----\n')
        #broadcast(msg, client)
    except:
        deleteClient(client)

def messagesTreatment1(client):
    while True:
        try:
            sleep(0.1)
            msg = client.recv(2048)
            aparelhos_book.ParseFromString(msg)
            print(aparelhos_book.ListFields())
            #broadcast(msg, client)
        except:
            continue
            
        
def messagesTreatment2(client):
    while True:
        try:
            sleep(0.1)
            msg = client.recv(2048)
            aparelhos_book.ParseFromString(msg)
            print(aparelhos_book.ListFields())
            #broadcast(msg, client)
        except:
            continue
            

def ligarLampada():
    aparelhos_book.Clear()
    aparelhos_book.aparelhos.name = 'lampada'
    aparelhos_book.aparelhos.on = 'L I G A D A'
    msg = aparelhos_book.SerializeToString()
    aparelhos_book.ParseFromString(msg)
    return msg

def desligarLampada():
    aparelhos_book.Clear()
    aparelhos_book.aparelhos.name = 'lampada'
    aparelhos_book.aparelhos.on = 'D E S L I G A D A'
    msg = aparelhos_book.SerializeToString()
    aparelhos_book.ParseFromString(msg)
    return msg

def ligarSom():
    aparelhos_book.Clear()
    aparelhos_book.aparelhos.name = 'som'
    aparelhos_book.aparelhos.on = 'L I G A D O'
    aparelhos_book.aparelhos.volume = '0'
    msg = aparelhos_book.SerializeToString()
    aparelhos_book.ParseFromString(msg)
    return msg

def desligarSom():
    aparelhos_book.Clear()
    aparelhos_book.aparelhos.name = 'som'
    aparelhos_book.aparelhos.on = 'D E S L I G A D O'
    aparelhos_book.aparelhos.volume = '0'
    msg = aparelhos_book.SerializeToString()
    aparelhos_book.ParseFromString(msg)
    return msg

def volumeSom(volume:str):
    aparelhos_book.Clear()
    aparelhos_book.aparelhos.name = 'som'
    aparelhos_book.aparelhos.on = 'L I G A D O'
    aparelhos_book.aparelhos.volume = volume
    msg = aparelhos_book.SerializeToString()
    aparelhos_book.ParseFromString(msg)
    return msg

def sendMessages():
    while True:
        try:
            sleep(0.1)
            escolha1 = input("Escolha funcao:\n1 - Lampada\n2 - Som\n3 - Chamada\n")
            if escolha1 == '1':
                escolha2 = input("1 - Ligar\n2 - Desligar\n")
                if escolha2 == '1':
                    msg = ligarLampada()
                if escolha2 == '2':
                    msg = desligarLampada() 
            if escolha1 == '2':   
                escolha2 = input("1 - Ligar\n2 - Desligar\n3 - Mudar volume\n")   
                if escolha2 == '1':
                    msg = ligarSom()
                if escolha2 == '2': 
                    msg = desligarSom()   
                if escolha2 == '3':   
                    novoVolume = input("Mudar para qual volume?\n")
                    msg = volumeSom(novoVolume) 
            if escolha1 == '3':  
                fazerChamada('Chamada') 
            
            
            for i in range(1,len(listaNome)):
                temp_host, temp_port = listaClient[i].getpeername()
                if listaNome[i] == 'lampada' and aparelhos_book.aparelhos.name == 'lampada':
                    if temp_port == listaPort[i]:
                        listaClient[i].send(msg)
                if listaNome[i] == 'som' and aparelhos_book.aparelhos.name == 'som':
                    if temp_port == listaPort[i]:
                        listaClient[i].send(msg)
            
            
            #comando = input("Digite o id do aparelho: ")
            
            ''''if(comando == '1'):
                for i in listaAparelhos:
                    print('1')
                    for j in i.aparelhos:
                        print('2')
                        if(j.name == 'lampada'):
                            print('3')
                            j.on = 'ligada'
                            msg = i.SerializeToString()
                    print(i.ListFields())
            comando = input("Digite o nome do aparelho: ")
            if comando == 'lampada':
                for i in range(1, len(listaAparelhos)):
                    if listaAparelhos[i].aparelhos.name == "lampada":
                        listaAparelhos[i].aparelhos.on = "ligada"
                        msg = listaAparelhos[i].SerializeToString()
                        print(listaAparelhos[i].ListFields())
                        temp_host, temp_port = client.getpeername()
                        if temp_port == listaPort[i]:
                            client.send(msg)'''
                            
                            
                            
                            
            #print(aparelhos_book.aparelhos.name)

            #picles = pickle.dumps(f'<{username}> {msg}')

            
        except:
            return

def fazerChamada(msg):
    data_string = str.encode(msg)
    print('\n---------------------------------')
    for i in range(1,len(listaClient)):
        listaClient[i].send(data_string)

        msg = listaClient[i].recv(2048)
        
        print(msg.decode())
    print('---------------------------------\n')

def deleteClient(client):
    listaClient.remove(client)

aparelhos_book = dispositivo_pb2.AparelhosBook()

main()