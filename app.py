#from cs50 import SQL
from flask import Flask, render_template, request
# from flask_session import Session
import openai, os
# from dotenv import load_dotenv

openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

# this route takes you to the index (main) page to input the question
# it will forward the prompt through the action form to answer.html 

@app.route("/")
def mainroute():
    return render_template("index.html")

@app.route('/chatgpt', methods=['GET'])
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
)        

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


@app.route('/wanted_image')
def generate_image2():
  domains_data[6]["visits"] += 1
  profile_url = request.args.get(
      'profile_url', 'https://telegra.ph/file/cd9ef2c65ea3e791cf419.jpg')
  img_bytes = create_image(profile_url)
  return send_file(img_bytes, mimetype='image/png')
    
    ##################################################


    @app.route('/gen_image')
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
