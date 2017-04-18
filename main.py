#-*-coding: utf-8-*-


import RPi.GPIO as GPIO
import time
from subprocess import Popen, PIPE, STDOUT
from conf import *
import time 
import telebot 
from telebot import *
from telebot import types
import sqlite3 
from threading import Timer
import os


creator = 102821769
knownUsers = []
userStep = {}
passaggio = {}
hideBoard = types.ReplyKeyboardRemove()
imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  #crea la tastiera per scegliere la foto
imageSelect.add('foto 1', 'foto 2')
rebootselect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
rebootselect.add('si','no')

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT) #inizializzo la gpio per il controllo manuale della ventola di raffreddamento

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        return 0

@bot.message_handler(commands=['shell'] ) #grazie @veetaw per avermi permesso di usare questo comando
def shell(message):
   if message.from_user.id == creator:
        command = " ".join(message.text.split(" ", 1)[1:])

        things = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT, close_fds=True)
        
        output = things.stdout.read()
        bot.send_message(message.chat.id, output)
   return

@bot.message_handler(commands=['temp'])
def temp(message):
    command = "./temperatura.sh"
    things = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = things.stdout.read()
    bot.send_message(message.chat.id, output)

@bot.message_handler(commands=['cpuload'])
def cpu(message):
    command = "sudo iostat -c 2 2"
    things = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = things.stdout.read()
    bot.send_message(message.chat.id, output)
        
        
    
@bot.message_handler(commands=['reboot'])
def reboot(message):
   if message.from_user.id == creator :
      cid = message.chat.id
      bot.reply_to(message, "Riavviare?", reply_markup=rebootselect)  # show the keyboard
      userStep[cid] = 2
      
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def msg_image_select(message):
      if message.text == "si":
         bot.reply_to(message, "riavviando....", reply_markup=hideBoard)
         os.system('sync')
         time.sleep(5)
         os.system('sudo reboot')
         userStep[cid] = 0
         
      elif message.text == "no":
         bot.reply_to(message, "Ok, resto acceso", reply_markup=hideBoard)
         userStep[cid] = 0
        
      else:
         bot.reply_to(message, "USA LA TASTIERA CHE TI HO DATO!!")
         bot.reply_to(message, "uff, riprova")
      
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  #se l'utente non ha ancora usato /start:
        knownUsers.append(cid)  # salva l'id dell'utente, in modo da poter mandare messaggi broadcast agli utenti del bot
        userStep[cid] = 0  
        bot.send_message(cid, "Ciao straniero! Rimani fermo, così posso analizzarti...")
        bot.send_chat_action(cid, 'typing')
        time.sleep(4)
        bot.send_message(cid, "Scansione completata! Non rappresenti una minaccia (spero)")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("gruppo per il mio sviluppo", url="https://t.me/joinchat/AAAAAEDGLP8YCxCwwR0NTA"))
        bot.reply_to(m, " <b>The PonzyBot </b>", reply_markup=markup, disable_web_page_preview=True,parse_mode="html" ) 

    else:
        bot.send_message(cid, "Ci conosciamo già... Pussa via!!")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("gruppo per la ricerca", url="https://t.me/joinchat/AAAAAEDGLP8YCxCwwR0NTA"))
        bot.reply_to(m, " <b>The PonzyBot </b>", reply_markup=markup, disable_web_page_preview=True,parse_mode="html" ) 


@bot.message_handler(commands=['foto'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "Scegli l'immagine", reply_markup=imageSelect)  # show the keyboard
    userStep[cid] = 1  #prepara l'utente per il prossimo passaggio 


# se l'utente ha usato /foto, questo gestisce la risposta
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_image_select(m):
    cid = m.chat.id
    text = m.text
    bot.send_chat_action(cid, 'typing')

    if text == "foto 1":
        bot.send_photo(cid, open('rooster.jpg', 'rb'),reply_markup=hideBoard) #invia il file e chiude la tastiera
        userStep[cid] = 0  # reimposta lo stato dell'utente
    elif text == "foto 2":
        bot.send_photo(cid, open('kitten.jpg', 'rb'), reply_markup=hideBoard)
        userStep[cid] = 0
    else:
        bot.send_message(cid, "USA LA TASTIERA CHE TI HO DATO!!")
        bot.send_message(cid, "uff, riprova")

@bot.message_handler(commands=['regole'])
def regole(message):
 if message.chat.id in legolisti:
   bot.reply_to(message,"""Questo gruppo è stato creato con lo scopo di permettervi di fare quello che il gruppo legolisti anonimi non vi permette di fare. Potete quindi chiedere suggerimenti per un MOC o su che set comprare mostrare le vostre opere / set e qualsiasi altra cosa riguardante i lego. Non è per fare concorrenza a legolize ma si spera aiuti a mantenere pulito il gruppo di FB da tutto ciò che non è Memas.
   *REGOLAMENTO*
   -Evitate di mandare tanti messaggi uno di fila all'altro. Cercate di fare un messaggio unico
   -Non sono concesse immagini gore, splatter e porno.
   -Non è concesso inviare più di una GIF o sticker consecutivo, in quanto potrebbero ostacolare la lettura del messaggio.
   -Cerchiamo di evitare il piu possibile l'off topic
   NB. *TUTTI* devono rispettare il regolamento!""", parse_mode="markdown")

 else: 
   bot.reply_to(message,"""
  *REGOLAMENTO*
   -Evitate di mandare tanti messaggi uno di fila all'altro. Cercate di fare un messaggio unico
   -Non sono concesse immagini gore, splatter e porno.
   -Non è concesso inviare più di una GIF o sticker consecutivo, in quanto potrebbero ostacolare la lettura del messaggio.
   -Cerchiamo di evitare il piu possibile l'off topic
   NB. *TUTTI* devono rispettare il regolamento!""", parse_mode="markdown")

      
@bot.message_handler(commands=['info'])
def info(message):
 try:
   if message.from_user.id in admins:
     if message.reply_to_message:
       bot.send_chat_action(message.chat.id, 'typing') 
       stato=bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id).status
       bot.reply_to(message, "*quello che so su di te*: \n*NOME:* {}\n*COGNOME:* {}\n *USERNAME:* @{}\n*ID:* {}".format(
       message.reply_to_message.from_user.first_name,
       message.reply_to_message.from_user.last_name,
       message.reply_to_message.from_user.username,
       str(message.reply_to_message.from_user.id)), parse_mode="markdown")

     else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, str(message.chat.id))
 except:
    pass

@bot.message_handler(commands=['ora'])
def ora(message):
   bot.send_chat_action(message.chat.id, 'typing')
   bot.reply_to(message, (time.strftime("%H:%M:%S")))  



@bot.message_handler(commands=['ciao','Ciao'])

def ciao(message):
  bot.send_chat_action(message.chat.id, 'typing')
  bot.reply_to(message, "Ciao, io sono @Ponzybot e sono stato creato da @P205T16. Se qualche volta non rispondo è perchè sono in manutenzione o semplicemente sono morto. beh, non ho molto da dirti al momento quindi   CIAONE")

@bot.message_handler(func=lambda m: True, content_types=['new_chat_member'])
def agg(m):
  if m.chat.id in officialchats:
         bot.send_message(m.chat.id,"Ciao {} benvenuto in questo gruppo, mi raccomando rispetta gli altri membri e non floodare stickers :D" .format(str(m.new_chat_member.first_name)), parse_mode="markdown")
         bot.send_message(creator, str(m.new_chat_member.first_name)+str(m.new_chat_member.last_name)+" si è unito al gruppo")  
  return
 
@bot.message_handler(func=lambda m: True)
def parolaacaso(m):
  if m.chat.id in officialchats:
    try:
      cos = str(m.reply_to_message.from_user.username)
      if m.text == "#ban":
        if m.from_user.id in admins:
          if m.reply_to_message:
            if m.reply_to_message.from_user.id not in admins:
              bot.kick_chat_member(m.chat.id, m.reply_to_message.from_user.id)
              bot.send_message(creator, str(m.reply_to_message.from_user.first_name)+"("+str(m.reply_to_message.from_user.username)+") *è stato bannato da *"+str(m.from_user.username), parse_mode="markdown")
           
      if m.text == "#kick":	
        if m.from_user.id in admins:
          if m.reply_to_message:
            if m.reply_to_message.from_user.id not in admins:
              bot.kick_chat_member(m.chat.id, m.reply_to_message.from_user.id)
              bot.unban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
              bot.send_message(creator, str(m.reply_to_message.from_user.first_name)+"("+str(m.reply_to_message.from_user.username)+") *è stato kickato da *@"+str(m.from_user.username), parse_mode="markdown")
     
      if m.text == "#unban":
        if m.from_user.id in admins:
          if m.reply_to_message:
            if m.reply_to_message.from_user.id not in admins:
              bot.unban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
              bot.send_message(creator, str(m.reply_to_message.from_user.username)+"("+str(m.reply_to_message.from_user.id)+") *è stato sbannato da *@"+str(m.from_user.username), parse_mode="markdown")
      if m.text == "#u":
        if m.from_user.id in admins:
          if m.reply_to_message:
            bot.send_message(m.chat.id, "@{} unisci i messaggi.".format(cos))
      if m.text == "#warn":
        if m.from_user.id in admins:
          if m.reply_to_message:
            bot.send_message(m.chat.id, "@{} stai rischiando il ban".format(cos))
      
    except:
      pass
  

  #serie di comandi botta risposta
  if m.text == "Grazie":
     bot.send_message(m.chat.id, "Prego")
  if m.text == "Maronne":
     bot.send_message(m.chat.id, "I kicks")
  if m.text == "grazie":
     bot.send_message(m.chat.id, "prego")
  
  if m.text == "thx":
     bot.send_message(m.chat.id, "np")
  if m.text == "Thx":
      bot.send_message(m.chat.id, "Np")
  if m.text == "sei acceso?":
     bot.send_message(m.chat.id, "SSSSI")
    
 

#gestione manuale della ventola
  if m.text == "Accendi":
     if m.from_user.id == creator:
        GPIO.output(21,True)
        bot.send_message(m.chat.id, "Ventola in funzione")
  if m.text == "Spegni":
     if m.from_user.id == creator:
        GPIO.output(21, False)
        bot.send_message(m.chat.id, "Ventola spenta")

bot.polling(none_stop=True)
