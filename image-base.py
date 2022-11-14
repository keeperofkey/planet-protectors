# coding: utf-8
import os
import numpy as np
import pandas as pd
import openai
import requests
from PIL import Image, ImageDraw, ImageFont
import random
import time

#possible intergration into Instagram
#from instabot import Bot
#bot = Bot()
#bot.login(username="", password="")
i=0
climate_concepts = []
image_descriptions = []
image_captions = []

openai.api_key = os.getenv("OPENAI_API_KEY")
while i < 264:
    concept = openai.Completion.create(
      model="text-davinci-002",
      prompt="Generate a concept about climate change:",
      temperature=1,
      max_tokens=32,
      top_p=1,
      frequency_penalty=1,
      presence_penalty=1
    )
    print(concept.choices[0].text.strip() + "\n")
    climate_concepts.append(concept.choices[0].text.strip())
    
    #this generates the prompt for DALL-E needs context/concept first
    scene = openai.Completion.create(
      model="text-davinci-002",
      prompt=concept.choices[0].text.strip() + "Describe an funny image that relates to this:",
      temperature=1,
      max_tokens=64,
      top_p=1,
      frequency_penalty=1,
      presence_penalty=1
    )
    print(scene.choices[0].text.strip() + "\n")
    image_descriptions.append(scene.choices[0].text.strip())
    
    #this writes the caption for the image described not sure impact of order here
    caption = openai.Completion.create(
      model="text-davinci-002",
      prompt=scene.choices[0].text.strip() + "Write a funny caption about this:",
      temperature=1,
      max_tokens=32,
      top_p=1,
      frequency_penalty=1,
      presence_penalty=1
    ) 
    print(caption.choices[0].text + "\n")
    image_captions.append(caption.choices[0].text.strip())
    #sprinkle of style
    lighting = ["Golden Hour", "Blue Hour", "Midday", "Overcast"]
    mood = ["Gothic","Surreal","Cyberpunk","Afrofuturism"]
    styles = ["Painting","Photograph","Rendering","Experimental","Drawing","Sculpture",]
    style =random.choice(styles) + ", " + random.choice(lighting) + ", " + random.choice(mood)
    print(style)
    prompt = scene.choices[0].text.strip() + "," + style
    #this calls DALLE to gen a single image
    image = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
    print(image.data[0].url)
    
    #this formats caption could have more cases
    f_caption = caption.choices[0].text.strip("\n")
    if len(f_caption) > 69:
        s = f_caption[:70] + "\n" + f_caption[70:]
        f_caption = s
    elif len(f_caption) > 138:
        sen = f_caption.split(" ")
        s = f_caption[:2]
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
    #bot.upload_photo(f_img, caption=concept.choices[0].text)
    #this creates dataframe by ziping lists together
    list_of_tuples = list(zip(climate_concepts, image_descriptions, image_captions))
    climate_change_images_df = pd.DataFrame(list_of_tuples, columns = ['Climate_Concept', 'Image_Description', 'Image_Caption'])
    climate_change_images_df.head()
    
    #write to json
    df_json = climate_change_images_df.to_json(orient='columns')
    print(df_json)
    f_data = "./data/data.json"
    with open(f_data, 'a') as handler:
        handler.write(df_json)
    i += 1
    if i == 24:
        time.sleep(300)
    if i == 48:
        time.sleep(300)
    if i == 72:
        time.sleep(300)
    if i == 96:
        time.sleep(300)
    if i == 120:
        time.sleep(300)
    if i == 144:
        time.sleep(300)

    if i == 168:
        time.sleep(300)
    if i == 192:
        time.sleep(300)
    if i == 216:
        time.sleep(300)
    if i == 240:
        time.sleep(300)
####Export to Excel###
#file_import_location = './data/'
##Create a Pandas Excel writer using XlsxWriter as the engine.
#writer = pd.ExcelWriter(file_import_location + 'climate_change_gpt3_image_data.xlsx', engine='xlsxwriter')
#
## Write each dataframe to a different worksheet.
#climate_change_images_df.to_excel(writer, sheet_name='Image_Data', index=False)
#
#
## Close the Pandas Excel writer and output the Excel file.
#writer.save()
