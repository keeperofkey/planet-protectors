# coding: utf-8
import os
import openai
import requests
from PIL import Image, ImageDraw, ImageFont

openai.api_key = os.getenv("OPENAI_API_KEY")
concept = "Climate change will result in environmental degradation, increased extreme weather conditions, and decreased resource availiblity. This will cause risks to human and ecosystem health and the viablity of infrastucture" 
#concept = openai.Completion.create(
#  model="text-davinci-002",
#  prompt="Generate a concept related to climate change:\n",
#  temperature=1,
#  max_tokens=64,
#  top_p=1,
#  frequency_penalty=1,
#  presence_penalty=1
#)
#print(concept.choices[0].text)
scene = openai.Completion.create(
  model="text-davinci-002",
  prompt="Describe a funny image representing this:\n" + concept,
  temperature=1,
  max_tokens=128,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
)
print(scene.choices[0].text)
caption = openai.Completion.create(
  model="text-davinci-002",
  prompt="Write a funny caption about this:\n" + scene.choices[0].text,
  temperature=1,
  max_tokens=64,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
) 
print(caption.choices[0].text)
image = openai.Image.create(prompt=scene.choices[0].text, n=1, size="1024x1024")
print(image.data[0].url)

img_data = requests.get(image.data[0].url).content
with open("./images/{}.jpg".format(caption.choices[0].text), 'wb') as handler:
    handler.write(img_data)
img = Image.open("./images/{}.jpg".format(caption.choices[0].text))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype('SourceCodePro-Black.otf', 24)
draw.multiline_text((0, 0), "{}".format(caption.choices[0].text), fill=(255, 0, 0), font=font)
img.save("./images/{}.jpg".format(caption.choices[0].text))
