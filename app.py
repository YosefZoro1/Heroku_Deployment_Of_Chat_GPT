from flask import Flask, request, jsonify, render_template, send_file, Response
from PIL import Image, ImageDraw, ImageFont
import openai, requests, random
from offices import char_dicts

char_dicts = char_dicts.Char_Dicts
from bs4 import BeautifulSoup
from kvsqlite.sync import Client
from translate import Translator
import json
from io import BytesIO
import arabic_reshaper, bidi.algorithm
from elevenlabs import set_api_key, generate, Voice

server = Flask(__name__)

domains_data = [
    {
        "domain": "ChatGPT",
        "visits": 0
    },
    {
        "domain": "decor",
        "visits": 0
    },
    {
        "domain": "insta",
        "visits": 0
    },
    {
        "domain": "que",
        "visits": 0
    },
    {
        "domain": "loque",
        "visits": 0
    },
    {
        "domain": "gen image",
        "visits": 0
    },
    {
        "domain": "wanted image",
        "visits": 0
    },
    {
        "domain": "IG save",
        "visits": 0
    },
    {
        "domain": "to speech",
        "visits": 0
    },
]


def Not_text():
  return jsonify({'result': 'Plz Enter Text'})


@server.route('/', methods=['GET'])
def home():
  return render_template("index-home.html")


##################################################
##################################################
##################################################


@server.route('/chatgpt', methods=['GET'])
def open_ai():
  domains_data[0]["visits"] += 1
  text = request.args.get('query', '')
  key = 'darkman|YVg3cyukPe8jSVBb8VuLT3BlbkFJlh0mhBk714FLEBOobPN1'
  i = (key).split('darkman|')[1]
  openai.api_key = f'sk-{i}'
  try:
    if text == '':
      return Not_text()

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=[{
                                                  "role": "user",
                                                  "content": text
                                              }])
    answer = completion.choices[0].message["content"]
    return jsonify({"result": answer})
  except Exception as e:
    return jsonify({
        'error': str(e),
        'result': 'An internal server error occurred'
    }), 500


##################################################


@server.route('/decor', methods=['GET'])
def decor_darco():
  domains_data[1]["visits"] += 1
  input_text = request.args.get('query', '')
  if input_text == '':
    return Not_text()

  results = []
  for char_dict in char_dicts:
    decorated_text = ''
    for char in input_text:
      found = False
      for char_key in char_dict.keys():
        if char.lower() == char_key:
          decorated_text += char_dict[char_key]
          found = True
          break
      if not found:
        decorated_text += char
    results.append(decorated_text)

  return jsonify({"result": results})


##################################################


@server.route('/insta', methods=['GET'])
def get_instagram_data():
  domains_data[2]["visits"] += 1
  target = request.args.get('query', '')

  if not target:
    return jsonify({"error": "Username must be provided"}), 400
  username = target

  url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}'

  headers = {
      'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
      'Cookie':
      'ig_did=FE857FA2-50E2-4412-9205-AFD556AC313B; ig_nrcb=1; mid=ZDAWPwALAAFNxlM9KwFP3jLaQ3kC; datr=rRYwZAFC-LaBsBCekyGPVduH; ds_user_id=47675279829; csrftoken=0VNXCy4bFu3vwedso6fsONvbPeGlY3Vp; sessionid=47675279829%3ACyLAsPHeA8XBs7%3A25%3AAYeDeNb7cAY0wyB0CQk0bLC13K2Gav7gXzCTiL14pQ; shbid="14281\05447675279829\0541731245278:01f7b8cde814936c5d2535e3d717d05f128df2e36b37709553bdadfb33922661aab5d39f"; shbts="1699709278\05447675279829\0541731245278:01f769156ff38adbc65dcb561941e80a130c4844e635ab9400ec7642602f17ee8c84f2a7"; rur="CLN\05447675279829\0541731245518:01f748af0c558f3af9fdb806a036e1abf37800c7846bacf74bf63badc2a95bd23e30316e"',
      'Dpr': '1',
      'Referer': f'https://www.instagram.com/{username}/',
      'Sec-Ch-Prefers-Color-Scheme': 'dark',
      'Sec-Ch-Ua':
      '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
      'Sec-Ch-Ua-Full-Version-List':
      '"Google Chrome";v="119.0.6045.124", "Chromium";v="119.0.6045.124", "Not?A_Brand";v="24.0.0.0"',
      'Sec-Ch-Ua-Mobile': '?0',
      'Sec-Ch-Ua-Model': '""',
      'Sec-Ch-Ua-Platform': '"Windows"',
      'Sec-Ch-Ua-Platform-Version': '"10.0.0"',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
      'Viewport-Width': '418',
      'X-Asbd-Id': '129477',
      'X-Csrftoken': '0VNXCy4bFu3vwedso6fsONvbPeGlY3Vp',
      'X-Ig-App-Id': '936619743392459',
      'X-Ig-Www-Claim':
      'hmac.AR1mGqbAXDS4qLXVl56NWM6cwzfZ8E_jnLgMQ4U-DqbkDirp',
      'X-Requested-With': 'XMLHttpRequest'
  }

  data_json = {}
  dk = requests.get(url, headers=headers)
  data = dk.json()

  data_json['id'] = (data['data']['user']['id'])
  data_json['profile pic'] = (data['data']['user']['profile_pic_url_hd'])
  data_json['full name'] = (data['data']['user']['full_name'])
  data_json['bio'] = (data['data']['user']['biography'])

  if "bio_links" in data['data']['user'] and len(
      data['data']['user']['bio_links']) > 0:
    first_bio_link = data['data']['user']['bio_links'][0]
    if "url" in first_bio_link:
      data_json['bio link'] = first_bio_link['url']
    else:
      data_json['bio link'] = None
  else:
    data_json['bio link'] = None

  data_json['posts'] = (
      data['data']['user']['edge_owner_to_timeline_media']['count'])
  data_json['follow'] = (data['data']['user']['edge_followed_by']['count'])
  data_json['following'] = (data['data']['user']['edge_follow']['count'])
  data_json['private'] = (data['data']['user']['is_private'])
  data_json['business account'] = (data['data']['user']['is_business_account'])
  data_json['professional account'] = (
      data['data']['user']['is_professional_account'])
  data_json['status'] = (data['status'])

  return jsonify({"result": data_json})


##################################################


@server.route('/que', methods=['GET'])
def Question():
  domains_data[3]["visits"] += 1
  text = request.args.get('query', '')
  if text != 'dark man':
    return jsonify({"result": 'An internal server error occurred'}), 500

  db = Client("database/ktweet.daddy")
  gg = []
  for i in db.keys():
    gg.append(i[0])
  gs = random.randint(1, 355)
  answer = (gg[gs])

  return jsonify({"result": answer})


##################################################


@server.route('/loque', methods=['GET'])
def loQuestion():
  domains_data[4]["visits"] += 1
  text = request.args.get('query', '')
  if text != 'dark man':
    return jsonify({"result": 'An internal server error occurred'}), 500

  db = Client("database/ah.daddy")
  translator = Translator(to_lang="ar")

  while True:
    # توليد مفتاح عشوائي
    random_key = str(random.randint(1, 489))  # ضبط النطاق حسب احتياجاتك
    # الحصول على القيمة للمفتاح العشوائي
    value = db.get(random_key)

    if value is not None:
      data = {}
      data['one'] = {
          'question': translator.translate(value['one']['question'])
      }
      data['two'] = {
          'question': translator.translate(value['two']['question'])
      }
      return jsonify({"result": data})
      break  # انهاء الحلقة عند العثور على قيمة صالحة


##################################################


@server.route('/gen_image')
def generate_image():
  domains_data[5]["visits"] += 1
  profile_url = request.args.get(
      'profile_url', 'https://telegra.ph/file/cd9ef2c65ea3e791cf419.jpg')
  second_profile_url = request.args.get(
      'second_profile_url',
      'https://telegra.ph/file/3694d5edde3846459647b.jpg')

  username = request.args.get('username')
  group = request.args.get('group')
  member = int(request.args.get('member'))

  reshape_text = arabic_reshaper.reshape(username)
  reshape_text2 = arabic_reshaper.reshape(group)
  reshape_text3 = arabic_reshaper.reshape(f'عـددنــا: {member}')
  bidi_text = bidi.algorithm.get_display(reshape_text)
  bidi_text2 = bidi.algorithm.get_display(reshape_text2)
  bidi_text3 = bidi.algorithm.get_display(reshape_text3)
  text_lines = [bidi_text, bidi_text2, bidi_text3]

  img_bytes = create_profile_image(profile_url, second_profile_url, text_lines)

  # Return the image as a response
  return Response(img_bytes, mimetype='image/png')


def create_profile_image(profile_url, second_profile_url, text_lines):
  # Load the background image
  background_path = 'database/background.png'
  background = Image.open(background_path).convert('RGBA')

  # Load first profile image
  profile_response = requests.get(profile_url)
  profile_response.raise_for_status()
  profile = Image.open(BytesIO(profile_response.content)).convert('RGBA')

  # Resize first profile image to 222x222 pixels
  profile = profile.resize((222, 222))

  # Define the relative position of the first profile image
  relative_position_x = 0.087
  relative_position_y = 0.213

  profile_position = (int(
      (background.width - profile.width) * relative_position_x),
                      int((background.height - profile.height) *
                          relative_position_y))

  # Create a mask for the circle
  mask = Image.new('L', (profile.width, profile.height), 0)
  draw = ImageDraw.Draw(mask)
  draw.ellipse((0, 0, profile.width, profile.height), fill=255)

  # Paste the first profile image using the mask
  background.paste(profile, profile_position, mask)

  # Load second profile image
  second_profile_response = requests.get(second_profile_url)
  second_profile_response.raise_for_status()
  second_profile = Image.open(BytesIO(
      second_profile_response.content)).convert('RGBA')

  # Resize second profile image to 162x162 pixels
  second_profile = second_profile.resize((162, 162))

  # Define the relative position of the second profile image
  second_relative_position_x = 0.92
  second_relative_position_y = 0.59

  second_profile_position = (int(
      (background.width - second_profile.width) * second_relative_position_x),
                             int((background.height - second_profile.height) *
                                 second_relative_position_y))

  # Create a mask for the circle
  second_mask = Image.new('L', (second_profile.width, second_profile.height),
                          0)
  second_draw = ImageDraw.Draw(second_mask)
  second_draw.ellipse((0, 0, second_profile.width, second_profile.height),
                      fill=255)

  # Paste the second profile image using the mask
  background.paste(second_profile, second_profile_position, second_mask)

  # Add text to the image
  draw = ImageDraw.Draw(background)
  font_size = 25
  font = ImageFont.truetype("database/Arial.ttf", font_size)

  # Calculate the position for each text line
  text_positions = [
      (background.width // 17, profile_position[1] + profile.height + 93),
      (background.width // 1.290, profile_position[1] + profile.height + 100),
      (background.width // 10, profile_position[1] + profile.height + 140)
  ]

  # Add text lines to the image
  for text, position in zip(text_lines, text_positions):
    draw.text(position, text, font=font, fill=(255, 255, 255, 255))

  # Convert the image to bytes
  img_bytes = BytesIO()
  background.save(img_bytes, format="PNG")
  img_bytes.seek(0)

  return img_bytes


##################################################


def create_image(profile_url):
  # Load the background image
  background_path = 'database/background2.png'
  background = Image.open(background_path).convert('RGBA')

  # Load the overlay image
  profile_response = requests.get(profile_url)
  profile_response.raise_for_status()
  profile = Image.open(BytesIO(profile_response.content)).convert('RGBA')

  # Resize overlay image
  size = (441, 441)
  profile = profile.resize(size, Image.LANCZOS)

  # Paste overlay image onto the background
  position = (148, 285)
  background.paste(profile, position, profile)

  # Save the result
  img_bytes = BytesIO()
  background.save(img_bytes, format="PNG")
  img_bytes.seek(0)

  return img_bytes


@server.route('/wanted_image')
def generate_image2():
  domains_data[6]["visits"] += 1
  profile_url = request.args.get(
      'profile_url', 'https://telegra.ph/file/cd9ef2c65ea3e791cf419.jpg')
  img_bytes = create_image(profile_url)
  return send_file(img_bytes, mimetype='image/png')


##################################################
@server.route('/instagramdl')
def instagramdl():
  domains_data[7]["visits"] += 1
  reel = request.args.get('qurey', '')
  url = 'https://vidinsta.app/web/home/fetch'
  headers = {
      "Accept": "text/html, */*; q=0.01",
      "Accept-Encoding": "identity;q=1, *;q=0",  #"gzip, deflate, br",
      "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
      "Cookie":
      "_csrf=0c6b1b278b7095293e8bc4695dd1091f8fbfa2514d8abb4369ee0579d5ba2b3da%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22CBrXo9IGCrIKivmlwzarr7eMQl703rNa%22%3B%7D; _ga_V3DS4P6657=GS1.1.1701613588.1.0.1701613588.0.0.0; _ga=GA1.1.302626962.1701613588; __gads=ID=92d242f839780292:T=1701613541:RT=1701613541:S=ALNI_MZ43H0MHddpxP3zL5IdT0zRsgPbPA; __gpi=UID=00000ce28d87d8f2:T=1701613541:RT=1701613541:S=ALNI_MacxKflLJS08Cwcp0UAE22yAW0XOA; _ga_C685S7JGC5=GS1.1.1701613588.1.0.1701613593.0.0.0",
      "Origin": "https://vidinsta.app",
      "Referer": "https://vidinsta.app/",
      "Sec-Ch-Ua":
      "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
      "Sec-Ch-Ua-Mobile": "?0",
      "Sec-Ch-Ua-Platform": "\"Windows\"",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-origin",
      "User-Agent":
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
      "X-Csrf-Token":
      "-gCkoW2dMnp4KsM6Hz9oMJgPCV-wRxIQvBN7kXbbBzq5Qtb5AqR7PTtYinF2SQVc73VoLcJwd13tf0yhRalJWw==",
      "X-Requested-With": "XMLHttpRequest",
  }

  data = {
      'url': reel,
      "type": "",
  }

  response = requests.post(url, headers=headers, data=data)
  print(response.status_code)
  print(response.text)
  soup = BeautifulSoup(response.text, 'html.parser')
  footer_div = soup.find('div', class_='col-xs-4 text-center')
  footer_div2 = soup.find('div', class_='col-sm-4 col-sm-pull-8')

  data = {}
  #video
  if footer_div:
    anchor_tag = footer_div.find('a')
    href_value = anchor_tag.get('href')
    vid = "https://vidinsta.app" + href_value
    data['video'] = (vid)

#image
  if footer_div2:
    anchor_tag = footer_div2.find('img')
    href_value = anchor_tag.get('src')
    img = "https://vidinsta.app" + href_value
    data['image'] = (img)
    print(data)

  return jsonify({"result": data})


##################################################


@server.route('/to-speech', methods=['GET'])
def text_to_speech():
  domains_data[8]["visits"] += 1

  dktext = request.args.get('query', '')
  apikey = request.args.get('apikey', '')
  if apikey == "":
    return jsonify({"error": "apikey is empty"})
  if dktext == "":
    return jsonify({"error": "text is empty"})

  set_api_key(f"{apikey}")

  audio = generate(text=dktext, voice="Adam", model="eleven_multilingual_v2")

  if audio:
    # احفظ البيانات الصوتية في ملف مؤقت
    audio_path = 'temp_audio.mp3'
    with open(audio_path, 'wb') as f:
      f.write(audio)

      return send_file(audio_path,
                       mimetype='audio/mp3',
                       as_attachment=False,
                       download_name='output.mp3')


##################################################


@server.route('/to-speech-v2', methods=['GET'])
def text_to_speech2():
  domains_data[8]["visits"] += 1

  dktext = request.args.get('query', '')
  apikey = request.args.get('apikey', '')
  if apikey == "":
    return jsonify({"error": "apikey is empty"})
  if dktext == "":
    return jsonify({"error": "text is empty"})

  set_api_key(f"{apikey}")

  audio = generate(text=dktext, voice="Mimi", model="eleven_multilingual_v2")

  if audio:
    audio_path = 'temp_audio2.mp3'
    with open(audio_path, 'wb') as f:
      f.write(audio)

      #tts
      return send_file(audio_path,
                       mimetype='audio/mp3',
                       as_attachment=False,
                       download_name='output2.mp3')


##################################################


@server.route("/stats", methods=["GET"])
def show_stats():
  return render_template("index-stats.html", domains_data=domains_data)


##################################################
if __name__ == '__main__':
  server.run(host='0.0.0.0', port=1337)
