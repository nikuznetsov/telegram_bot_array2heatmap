import matplotlib.pyplot as plt # Plotting
import numpy as np # Arrays
import os
# Подключаем модуль случайных чисел 
import random
# Подключаем модуль для Телеграма
import telebot
# Указываем токен
# Импортируем типы из модуля, чтобы создавать кнопки
from telebot import types

@bot.message_handler(content_types=['document'])
def handle_file(message): 
    chat_id = message.chat.id
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = 'C:/Users/Nikita/Desktop/BOT/' + message.document.file_name
    length = len(file_info.file_path)
    if file_info.file_path[length-4:length+1] != ".dat":
        bot.send_message(message.from_user.id, "Ещё девяти утра нет, а вы уже злодействуете. Напишите лучше /help.")
    else:
        bot.reply_to(message, 'Немного магии...')
        points = np.array([]) # Array of plotting points
        perm = np.array([]) # Helping array
        line_counter = 0 # Lines counter
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)        
        with open(src) as file:  
            for line in file: # Cycle along lines in files
                line_counter += 1 # Counting lines
                if line_counter > 2: # Skip 3 first lines
                    line = np.array(line.strip(' ').split()) # Splitting by spaces
                    if line[0] == 'I=': # New line
                        perm = perm.flatten() # 1D array
                        if len(points) == 0: 
                            points = np.append(points, perm) # Append if it is empty
                        else:
                            points = np.vstack((points, perm)) # Stack if not empty
                        perm = np.array([]) # Nulling array
                    else:
                        line = line.astype(float) # Needed data type
                        perm = np.append(perm, line) # Fill in helping array
            # Append last line
            perm = perm.flatten()
            if len(points) == 0:
                points = np.append(points, perm)
            else:
                points = np.vstack((points, perm))
        plt.figure(figsize=(8,8)) # Size of picture
        plt.imshow(points.T, cmap='hot', interpolation='nearest') # сmap = 'hot' - color of picture, points.T - transposed array
        cbar = plt.colorbar() # Color bar
        cbar.ax.tick_params(labelsize=16) # Digits size
        cbar.ax.yaxis.get_offset_text().set(size=16) # Size of power on colorbar
        cbar.set_label('E-field amplitude', fontsize=16) # Size of label and label itself on colorbar
        plt.title(message.document.file_name) # Title
        plt.xlabel('z (nm)', fontsize=16) # Size and title of X
        plt.ylabel('x (nm)', fontsize=16) # Size and title of Y
        h, w = points.shape # Boundaries of picture
        plt.xlim(0,h) # X limits
        plt.ylim(w,0) # Y limits
        plt.savefig('C:/Users/Nikita/Desktop/BOT/{}.png'.format(message.document.file_name))
        plt.close()
        bot.send_message(message.from_user.id, "Max value for {} = {:.2e}".format(message.document.file_name, np.amax(points)))
        uis_png = open('C:/Users/Nikita/Desktop/BOT/{}.png'.format(message.document.file_name), 'rb')     
        bot.send_photo(message.from_user.id, uis_png)
        uis_png.close() 
        os.remove('C:/Users/Nikita/Desktop/BOT/{}.png'.format(message.document.file_name))
        os.remove('C:/Users/Nikita/Desktop/BOT/' + message.document.file_name)   
        bot.send_message(message.from_user.id, text='Можете прислать ещё файл... Или прощаемся.')

# Метод, который получает сообщения и обрабатывает их
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Инструкция:\nОтправьте текстовый файл формата KARAT с расширением .dat.\n\n\nДоступные команды:\n/start\n/help\n\n\nПо всем вопросам и предложениям:\n @nikuznetsov")
    elif message.text == "/start":
        bot.send_message(message.from_user.id, "Привет! Пришли мне файл!")        
    else:
        bot.send_message(message.from_user.id, "Ещё девяти утра нет, а ты вы злодействуете. Напишите лучше /help.")

bot.polling(none_stop=True, interval=0)