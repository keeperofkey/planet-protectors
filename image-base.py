# coding: utf-8
import os
import openai
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")

concept = openai.Completion.create(
  model="text-davinci-002",
  prompt="Here is a concept about climate change:\n",
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
print(concept.choices[0].text)
scene = openai.Completion.create(
  model="text-davinci-002",
  prompt = concept.choices[0].text + "Describe a funny image that represents this:\n",
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
print(scene.choices[0].text)
caption = openai.Completion.create(
  model="text-davinci-002",
  prompt = concept.choices[0].text + scene.choices[0].text + "With a funny caption:\n",
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
) 
print(caption.choices[0].text)
image = openai.Image.create(prompt=scene.choices[0].text, n=1, size="1024x1024")
print(image.data[0].url)

img_data = requests.get(image.data[0].url).content
with open("./images/{}.jpg".format(caption.choices[0].text), 'wb') as handler:
    handler.write(img_data)



