from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from planningCenter import getNames
from pypco import PCO
import requests
from getConfig import getConfig
from datetime import datetime
import pytz
import json

def adding_text(img, text, position, size, colour, font):
	 font = ImageFont.truetype(font, size)
	 W, H = position
	 draw = ImageDraw.Draw(img)
	 _, _, w, h = draw.textbbox((0, 0), text, font=font)
	 draw.text(((W-w)/2, (H-h)/2), text, font=font, fill=colour)
	 return img

def generateThumb():
	name, sermonTitle, theme = getNames()
        config = getConfig()
        
	pco = PCO(config['PlanningCenterAppID'],config['PlanningCenterAppSecret'])
	
	ervice_type_id =  ''

        response = pco.get('https://api.planningcenteronline.com/services/v2/service_types')
        for i in response['data']:
                if i['attributes']['name'] == 'Sabbath Service':
                        service_type_id = i['id']
	
        api = 'https://api.planningcenteronline.com/services/v2/service_types/' + service_type_id + '/plans'

	searched_plans = pco.get(api + '?filter=future&per_page=1')
	
	current_plan = pco.get(api + '/' + searched_plans['data'][0]['id'])
	attachments = current_plan['data']['links']['attachments']
	attachments = pco.get(attachments)
	if False: #attachments['data']!=[]:
		image = attachments['data'][0]['attributes']
		r=requests.get(image)
		img=Image.open(BytesIO(r.content)).convert('RGBA')
		imgpath=img.save('thumb.png')
	else:
		unsplash_token = config['UnsplashAppID']
		r = requests.get('https://api.unsplash.com/photos/random?client_id='+unsplash_token+'&query=landscape')
		raw_image = requests.get(json.loads(r.content)['urls']['raw']).content
		resized_image = requests.get(json.loads(r.content)['urls']['raw']+'&w=1280').content
		img = Image.open(BytesIO(resized_image)).convert('RGBA').resize((1280,720))
		template_image=Image.open('thumb-template.png').convert('RGBA')
		dark = Image.new(mode="RGBA", size=(1280, 720), color=(0, 0, 0, 50))
		generated = Image.alpha_composite(img, dark)
		generated = Image.alpha_composite(generated, template_image)
		generated = adding_text(generated, config['ChurchName'], (1280, 500), 30, (255, 255, 255), 'Montserrat/static/Montserrat-Regular.ttf')
		generated = adding_text(generated, '"' + sermonTitle + '"', (1280, 720), 65, (255, 255, 255), 'Aleo/Aleo-Regular.ttf')
		generated = adding_text(generated, name, (1280, 900), 30, (255, 255, 255), 'Montserrat/static/Montserrat-Regular.ttf')
		imgpath = generated.save('thumb.png')

	#localStartTime = datetime.strptime(datetime.strftime(datetime.now(), "%Y-%W") + '-6 10:45:00',>
	#utcStartTime = pytz.timezone("Australia/Sydney").localize(localStartTime, is_dst=None).astimez>
	#print("Sheduling Livestream for: " + localStartTime.strftime("%d %B %Y"))

	localStartTime = datetime.strptime(datetime.strftime(datetime.now(), "%Y-%W") + '-6 10:45:00', "%Y-%W-%w %H:%M:%S")
	utcStartTime = pytz.timezone("Australia/Sydney").localize(localStartTime, is_dst=None).astimezone(pytz.utc)
	print("Sheduling Livestream for: " + localStartTime.strftime("%d %B %Y"))

	return(imgpath)
