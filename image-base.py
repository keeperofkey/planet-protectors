# coding: utf-8
import os
import openai
import requests
from PIL import Image, ImageDraw

openai.api_key = os.getenv("OPENAI_API_KEY")

concept = openai.Completion.create(
  model="text-davinci-002",
  prompt="climate change is ",
  temperature=1,
  max_tokens=64,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
)
print(concept.choices[0].text)
scene = openai.Completion.create(
  model="text-davinci-002",
  prompt = concept.choices[0].text + "Describe an image that represents this:\n",
  temperature=0.7,
  max_tokens=128,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
)
print(scene.choices[0].text)
caption = openai.Completion.create(
  model="text-davinci-002",
  prompt = concept.choices[0].text + scene.choices[0].text + "With a funny caption:\n",
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
) 
print(caption.choices[0].text)
image = openai.Image.create(prompt=scene.choices[0].text, n=1, size="1024x1024")
print(image.data[0].url)

img_data = requests.get(image.data[0].url).content
print(img_data)

#draw = ImageDraw.Draw(img_data)
#draw.text((28, 36), "{}".format(caption.choices[0].text), fill=(255, 0, 0))
with open("./images/{}.jpg".format(caption.choices[0].text), 'wb') as handler:
    handler.write(img_data)



