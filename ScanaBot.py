import socket
import random
 
servidor = "localhost"
canal = "#canal"
nickName = ""
puerto = 6667
def name_generator():
	cad= "abcdefghijklmnopqrstuvwxyz1234567890"
	lenght= random.randint(4,10)
	name=[]
	name+=[cad[random.randint(0,len(cad))] for i in range(0,lenght)]
	return "".join(name)

def send_msg(canal , msg):
      irc.send("PRIVMSG "+ canal +" :"+ msg +"\n\r") 
      
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
 
#Modo Verboso para chat
def v_chat(ircmsg, canal):
      print (get_nick(canal, ircmsg)+": "+get_msg(canal, ircmsg))
      
nickName=name_generator()
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((servidor, puerto))
irc.send("USER "+ nickName +" "+ nickName +" "+ nickName +" :r\n\r")
irc.send("NICK "+ nickName +"\n\r")
print "Conectando..."
irc.send("JOIN "+ canal +"\n\r")
print "Se ha unido al canal " +canal

while 1:
      ircmsg = irc.recv(512)
      ircmsg = ircmsg.strip('\n\r')
      
      if ircmsg.find("PRIVMSG "+canal) != -1:
            v_chat(ircmsg, canal)
      
      if ircmsg.find("Hola") != -1:
            send_msg(canal, "Hola!!!")