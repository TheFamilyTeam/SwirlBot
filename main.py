import telepot
import random
import time
import os
import json

token = "YOUR_TOKEN:HERE"
bot = telepot.Bot(token)

queue = {
	"free":[],
	"occupied":{}
}

def saveConfig(data):
	return open('config.json', 'w').write(json.dumps(data))

if __name__ == '__main__':
	s = time.time()
	print('[#] Swirlbot 2\n[i] Created by TheFamilyTeam - @TheFamilyTeam\n')
	print('[#] Checking config...')
	if not os.path.isfile('config.json'):
		print('[#] Creating config file...')
		open('config.json', 'w').write('{}')
		print('[#] Done')
	else:
		print('[#] Config found!')
	print('[i] Bot online ' + str(time.time() - s) + 's')
def exList(list, par):
	a = list
	a.remove(par)
	return a

def handle(update):
	global queue
	try:
		config = json.loads(open('config.json', 'r').read())
		if 'text' in update:
			text = update["text"]
		else:
			text = ""
		uid = update["from"]["id"]

		if not uid in config and text != "/nopics":
			config[str(uid)] = {"pics":True}
			saveConfig(config)

		if uid in queue["occupied"]:
			if 'text' in update:
				if text != "/end":
					bot.sendMessage(queue["occupied"][uid], "Stranger: " + text)
			
			if 'photo' in update:
				if config[str(queue["occupied"][uid])]["pics"]:
					photo = update['photo'][0]['file_id']
					bot.sendPhoto(queue["occupied"][uid], photo)
					bot.sendMessage(queue["occupied"][uid], "Stranger sends you a photo!")
				else:
					bot.sendMessage(queue["occupied"][uid], "Stranger tried to send you a photo, but you disabled this,  you can enable photos by using the /nopics command")
					bot.sendMessage(uid, "Stranger disabled photos, and will not receive your photos")

			if 'video' in update:
				video = update['video']['file_id']
				bot.sendVideo(queue["occupied"][uid], video)
				bot.sendMessage(queue["occupied"][uid], "Stranger sends you a video!")

			if 'sticker' in update:
				sticker = update['sticker']['file_id']
				bot.sendDocument(queue["occupied"][uid], sticker)
				bot.sendMessage(queue["occupied"][uid], "Stranger sends you a sticker!")

		if text == "/end" and uid in queue["occupied"]:
			print('[SB] ' + str(uid) + ' left the conversation with ' + str(queue["occupied"][uid]))
			bot.sendMessage(uid, "Your conversation is over, I hope you enjoyed it :)")
			bot.sendMessage(uid, "Type /start to get matched with a new partner")
			bot.sendMessage(uid, "We're ending the conversation...")
			bot.sendMessage(queue["occupied"][uid], "Your conversation is over, I hope you enjoyed it :)")
			bot.sendMessage(queue["occupied"][uid], "Your conversation partner left the chat")
			del queue["occupied"][queue["occupied"][uid]]
			del queue["occupied"][uid]

		if text == "/start":
			if not uid in queue["occupied"]:
				bot.sendMessage(uid, 'Looking for a stranger to match you with... Hold on!')
				print("[SB] " + str(uid) + " joined the queue")
				queue["free"].append(uid)

		if text == "/help":
			bot.sendMessage(uid, "Help:\n\nUse /start to start looking for a conversational partner, once you're matched you can use /end to end the conversation.\n\nIf you have any questions or require help, join @TFChat or ask @borzetta.\n@TheFamilyTeam")

		if text == "/nopics":
			config[str(uid)]["pics"] = not config[str(uid)]["pics"] 
			if config[str(uid)]["pics"]:
				bot.sendMessage(uid, "Strangers can now send you photos!")
			else:
				bot.sendMessage(uid, "Strangers won't be able to send you photos anymore!")
			saveConfig(config)

		if len(queue["free"]) > 1 and not uid in queue["occupied"]:
			partner = random.choice(exList(queue["free"], uid))
			if partner != uid:
				print('[SB] ' + str(uid) + ' matched with ' + str(partner))
				queue["free"].remove(partner)
				queue["occupied"][uid] = partner
				queue["occupied"][partner] = uid
				bot.sendMessage(uid, 'You have been matched, have fun!')
				bot.sendMessage(partner, 'You have been matched, have fun!')
	except 	Exception as e:
		print('[!] Error: ' + str(e))

if __name__ == '__main__':
	bot.message_loop(handle)

	while True:
		time.sleep(10)
