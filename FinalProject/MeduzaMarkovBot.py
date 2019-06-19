import requests
from pyquery import PyQuery as pq
from tqdm import tqdm
import nltk
import re
import markovify
import random
import telebot
import conf
#import PySocks

#telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}
bot = telebot.TeleBot(conf.TOKEN)

bot.remove_webhook()

url_t = "https://meduza.io/api/w4/search?chrono=news&page={page}&per_page=24&locale=ru"

articles = []
for page in range(1, 15):
    url = url_t.format(page = page)
    print(url)
    res = requests.get(url)
articles.extend(res.json()["collection"])

for i in articles:
    for num, article_url in tqdm(enumerate(articles)):
        res = requests.get("https://meduza.io/" + article_url)
        title = ""
        for title in pq(res.text).find("h1.SimpleTitle-root"):
            title = pq(title).text().replace("\xa0", " ")
        text = ""
        for paragraph in pq(res.text).find("div.GeneralMaterial-article p"):
            text += pq(paragraph).text().replace("\xa0", " ")
        try:
            with open(f"texts_meduza/allthetexts.txt", "a", encoding="utf-8") as f:
                 f.write(text)
        except UnicodeEncodeError as err:
            print(err, article_url)
            
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Здравствуй, мудрая Медуза!')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
   bot.send_message(message.chat.id, "Здравствуй, заблудшая душа! Я здесь, чтобы помочь тебе заглянуть в свое будущее" + 
                        " и найти ответы на насущные вопросы. Меня зовут Медуза, и я умею читать знаки судьбы.",
                         reply_markup=keyboard1)

with open("texts_meduza/allthetexts.txt", encoding='utf-8') as f:
    text = f.read()

text_model = markovify.Text(text)
class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence
    
keyboard2 = telebot.types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = telebot.types.KeyboardButton('Еще предсказание!')
itembtn2 = telebot.types.KeyboardButton('Надоело, верни деньги!')
keyboard2.add(itembtn1, itembtn2)

@bot.message_handler(func=lambda x: x.text in ['Здравствуй, мудрая Медуза!',
                                               'Еще предсказание!',])
def blah(message):
    with open('texts_meduza/cheers.txt', encoding='utf-8') as f:
        fin = f.read()
        fin = fin.replace('\uffef', '')
        fin = fin.split('|')
        fin = random.choice(fin)

    with open('texts_meduza/wisdom.txt', encoding='utf-8') as f:
        ball = f.read()
        ball = ball.replace('\uffef', '')
        ball = ball.split('|')
        ball = random.choice(ball)
    
    for i in range(1):
        result = (text_model.make_short_sentence(200))
        reply = (ball + "\n" + '"' + result + '"' + "\n" + fin)
            
    bot.send_message(message.chat.id, text = 'Посмотрим, что о тебе расскажут знаки.')        
    bot.send_message(message.chat.id, text = reply, reply_markup=keyboard2)
    
@bot.message_handler(func=lambda x: x.text in ['Надоело, верни деньги!'])
def stop(message):
    bot.send_message(message.chat.id, text = 'Ха-ха, мои услуги бесплатны!' +
                     'Одумаешься - пиши "/start".')

@bot.message_handler(func=lambda m: True)
def smth(message):
    bot.send_message(message.chat.id, 'Я не понимаю твоих слов',
                      reply_markup=keyboard2)
    
    
        
if __name__ == '__main__':
    bot.polling(none_stop=True)
#bot.polling()
