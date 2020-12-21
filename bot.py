# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt 
import numpy as np
import redis
import os
import telebot
import random
from telebot import types
# import some_api_lib
# import ...

# Example of your code beginning
#           Config vars
token = os.environ['TELEGRAM_TOKEN']
some_api_token = os.environ['SOME_API_TOKEN']
#             ...

# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
r = redis.from_url(os.environ.get("REDIS_URL"))

bot = telebot.TeleBot('TELEGRAM_TOKEN')

#       Your bot code below
@bot.message_handler(content_types=['document'])
def handle_file(message): 
    chat_id = message.chat.id
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = '/app/' + message.document.file_name
    length = len(file_info.file_path)
    if file_info.file_path[length-4:length+1] != ".dat":
        bot.send_message(message.from_user.id, "Better check /help.")
    else:
        bot.reply_to(message, 'Magic...')
        points = np.array([]) 
        perm = np.array([]) 
        line_counter = 0 
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)        
        with open(src) as file:  
            for line in file: 
                line_counter += 1
                if line_counter > 2:
                    line = np.array(line.strip(' ').split())
                    if line[0] == 'I=': 
                        perm = perm.flatten()
                        if len(points) == 0: 
                            points = np.append(points, perm) 
                        else:
                            points = np.vstack((points, perm))
                        perm = np.array([])
                    else:
                        line = line.astype(float) 
                        perm = np.append(perm, line) 
            # Append last line
            perm = perm.flatten()
            if len(points) == 0:
                points = np.append(points, perm)
            else:
                points = np.vstack((points, perm))
        plt.figure(figsize=(8,8)) 
        plt.imshow(points.T, cmap='hot', interpolation='nearest') 
        cbar = plt.colorbar() 
        cbar.ax.tick_params(labelsize=16) 
        cbar.ax.yaxis.get_offset_text().set(size=16) 
        cbar.set_label('E-field amplitude', fontsize=16) 
        plt.title(message.document.file_name) 
        plt.xlabel('z (nm)', fontsize=16) 
        plt.ylabel('x (nm)', fontsize=16) 
        h, w = points.shape 
        plt.xlim(0,h) 
        plt.ylim(w,0) 
        plt.savefig('/app/{}.png'.format(message.document.file_name))
        plt.close()
        bot.send_message(message.from_user.id, "Max value for {} = {:.2e}".format(message.document.file_name, np.amax(points)))
        uis_png = open('/home/nikuznetsov/BOT/{}.png'.format(message.document.file_name), 'rb')     
        bot.send_photo(message.from_user.id, uis_png)
        uis_png.close() 
        os.remove('/app/{}.png'.format(message.document.file_name))
        os.remove('/app/' + message.document.file_name)   
        bot.send_message(message.from_user.id, text='You can send another file... Or bye!')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Instruction:\nSend text file in format KARAT with .dat. You can send multiple files at the same time.\n\nCommands:\n/start\n/help\n\nContacts:\n @nikuznetsov")
    elif message.text == "/start":
        bot.send_message(message.from_user.id, "Hello! Send me file!")        
    else:
        bot.send_message(message.from_user.id, "Better check /help.")

bot.polling(none_stop=True, interval=0)
