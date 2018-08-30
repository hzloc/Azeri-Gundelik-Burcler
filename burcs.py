import requests,re
from bs4 import BeautifulSoup
import json
from telegram.ext import Updater,MessageHandler,Filters,CommandHandler,Dispatcher,CallbackQueryHandler
import requests
from telegram import InlineKeyboardMarkup,InlineKeyboardButton


def between(value, a, b):
    # Find and validate before-part.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    # Find and validate after part.
    pos_b = value.rfind(b)
    if pos_b == -1: return ""
    # Return middle part.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= pos_b: return ""
    return value[adjusted_pos_a:pos_b]

def before(value, a):
    # Find first part and return slice before it.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    return value[0:pos_a]

def after(value, a):
    # Find and validate first part.
    pos_a = value.rfind(a)
    if pos_a == -1: return ""
    # Returns chars after the found string.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= len(value): return ""
    return value[adjusted_pos_a:]

def urlfinder():
	req = requests.get("https://www.milli.az/horoscope/")
	soup = BeautifulSoup(req.content, "lxml")
	content = soup.find('ul',class_="post-list2").a["href"]
	return "{}".format(content)

def lastarticle(url):
	req = requests.get(url)
	soup = BeautifulSoup(req.content, "lxml")
	articles = soup.find("div",class_="article_text").text
	articles = re.sub(r"Milli(.*?)edir.","",articles)
	articles = articles.replace('Milli.Az','')
	articles = re.sub(r"window(.*?)\};",'',articles)
	articles = articles.replace('\n', '')
	return articles

def splitsigns(articles):
	qoch = before(articles,"Buğa")
	buga = between(articles,"Buğa","Əkizlər")
	ekizler = between(articles,"Əkizlər","Xərçəng")
	xerceng = between(articles,"Xərçəng","Şir")
	shir = between(articles,"Şir","Qız")
	qiz = between(articles,"Qız","Tərəzi")
	terezi = between(articles,"Tərəzi","Əqrəb")
	eqreb = between(articles,"Əqrəb","Oxatan")
	oxatan = between(articles,"Oxatan","Oğlaq")
	oglaq = between(articles,"Oğlaq","Dolça")
	dolcha = between(articles,"Dolça","Balıqlar")
	baliqlar = after(articles,"Balıqlar")
	dict = {
            'qoch': qoch,
            'buga': buga,
            'ekizler': ekizler,
			'xerceng': xerceng,
			'shir': shir,
			'qiz': qiz,
			'terezi': terezi,
			'eqreb': eqreb,
			'oxatan': oxatan,
			'oglaq': oglaq,
			'dolcha': dolcha,
			'baliqlar': baliqlar
        }
	return dict
	
web = urlfinder()
article = lastarticle(web)
signs = splitsigns(article)



updater = Updater(token="632758802:AAFB7ykwVhQ1hZRgMuMmBysQVaiIIKiePSk")
dispatcher = updater.dispatcher


def zodiacsigns(bot,update):
	options = [
			[InlineKeyboardButton("Qoç",callback_data="qoch")],
			[InlineKeyboardButton("Buğa",callback_data="buga")],
			[InlineKeyboardButton("Əkizlər",callback_data="ekizler")],
			[InlineKeyboardButton("Xərçəng",callback_data="xerceng")],
			[InlineKeyboardButton("Şir",callback_data="shir")],
			[InlineKeyboardButton("Qız",callback_data="qiz")],
			[InlineKeyboardButton("Tərəzi",callback_data="terezi")],
			[InlineKeyboardButton("Əqrəb",callback_data="eqreb")],
			[InlineKeyboardButton("Oxatan",callback_data="oxatan")],
			[InlineKeyboardButton("Oğlaq",callback_data="oglaq")],
			[InlineKeyboardButton("Dolça",callback_data="dolcha")],
			[InlineKeyboardButton("Balıqlar",callback_data="baliqlar")]
				]
	reply = InlineKeyboardMarkup(options)
	bot.send_message(chat_id=update.message.chat_id,text="Xaiş edirik bürcünüzü seçəsiz: ",reply_markup=reply)

dispatcher.add_handler(CommandHandler("List", zodiacsigns))

def horoscopes(bot,update):
	data = update.callback_query.data
	text = "" 
	if (data == "qoch"):
		text = signs["qoch"]
	elif (data == "buga"):
		text = '*Buğa*\n'+signs["buga"]
	elif (data == "ekizler"):
		text = '*Əkizlər*\n'+signs["ekizler"]
	elif (data == "xerceng"):
		text = '*Xərçəng*\n'+signs['xerceng']
	elif (data == "shir"):
		text = '*Şir*\n'+signs['shir']
	elif (data == "qiz"):
		text = '*Qız*\n'+signs['qiz']
	elif (data == "terezi"):
		text = '*Tərəzi*\n'+signs['terezi']
	elif (data == "eqreb"):
		text = '*Əqrəb*\n'+signs['eqreb']
	elif (data == "oxatan"):
		text = '*Oxatan*\n'+signs['oxatan']
	elif (data == "oglaq"):
		text = '*Oğlaq*\n'+signs['oglaq']
	elif (data == "dolcha"):
		text = '*Dolça*\n'+signs["dolcha"]
	elif (data == "baliqlar"):
		text = '*Balıqlar*\n'+signs['baliqlar']
	bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
							text=text,message_id=update.callback_query.message.message_id)

dispatcher.add_handler(CallbackQueryHandler(horoscopes))

updater.start_polling()
updater.idle()

