# coding: utf-8
import os
import numpy as np
import pandas as pd
import openai
import requests
from PIL import Image, ImageDraw, ImageFont
import random

climate_concepts = []
image_descriptions = []
image_captions = []

openai.api_key = os.getenv("OPENAI_API_KEY")
#concept = "Climate change will result in environmental degradation, increased extreme weather conditions, and decreased resource availiblity. This will cause risks to human and ecosystem health and the viablity of infrastucture" 
concept = openai.Completion.create(
  model="text-davinci-002",
  prompt="Generate a concept related to climate change:\n",
  temperature=1,
  max_tokens=64,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
)
print(concept.choices[0].text)
climate_concepts.append(concept.choices[0].text.strip())

#this generates the prompt for DALL-E needs context/concept first
scene = openai.Completion.create(
  model="text-davinci-002",
  prompt=concept.choices[0].text + "Describe a funny image about this:\n",
  temperature=1,
  max_tokens=128,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
)
print(scene.choices[0].text)
image_descriptions.append(scene.choices[0].text.strip())

#this writes the caption for the image described not sure impact of order here
caption = openai.Completion.create(
  model="text-davinci-002",
  prompt=scene.choices[0].text + "Write a funny caption about this:\n",
  temperature=1,
  max_tokens=64,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
) 
print(caption.choices[0].text)
image_captions.append(caption.choices[0].text.strip())
#sprinkle of style
styles = ["Gothic","Surreal","Painting","Photograph","Rendering"]
style = random.choice(styles)
prompt = scene.choices[0].text + "," + style
#this calls DALLE to gen a single image
image = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
print(image.data[0].url)

#this formats caption could have more cases
f_caption = caption.choices[0].text.strip()
if len(f_caption) > 69:
    s = f_caption[:70] + "\n" + f_caption[70:]
    f_caption = s
#this downloads image locally
f_img = "./images/{}.jpg".format(f_caption)
img_data = requests.get(image.data[0].url).content
with open(f_img, 'wb') as handler:
    handler.write(img_data)
#this reopens image for edits, selects font, draws caption box, writes caption, saves
img = Image.open(f_img)
draw = ImageDraw.Draw(img)
font = ImageFont.truetype('SourceCodePro-Black.otf', 24)
draw.line((0,992) + (1024,992), fill=0, width=64)
draw.text((0, 960), "{}".format(f_caption), fill=(255, 0, 0), font=font)
img.save(f_img)

#this creates dataframe by ziping lists together
list_of_tuples = list(zip(climate_concepts, image_descriptions, image_captions))
climate_change_images_df = pd.DataFrame(list_of_tuples, columns = ['Climate_Concept', 'Image_Description', 'Image_Caption'])
climate_change_images_df.head()

###Export to Excel###

#Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(file_import_location + 'climate_change_gpt3_image_data.xlsx', engine='xlsxwriter')

# Write each dataframe to a different worksheet.
climate_change_images_df.to_excel(writer, sheet_name='Image_Data', index=False)


# Close the Pandas Excel writer and output the Excel file.
writer.save()
