# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 14:20:22 2022

"""

import pandas as pd
import numpy as np
import openai
import os
import json
from PIL import Image, ImageFont, ImageDraw
import re
import requests

#source: https://www.youtube.com/watch?v=VTx0xBPOv5Q
#Source2: https://www.youtube.com/watch?v=9971sxBhEyQ
#source3 jsonl: https://colab.research.google.com/drive/154FWlYVGbvLoYiSWCCeNy5XskskUzRQ3?usp=sharing#scrollTo=ETdV0OyYPFYZ

#engines
#"davinci-instruct-beta"
#"text-davinci-002"

api_key = '<<insert API key>>'
org = '<<insert org>>'

openai.organization = org
openai.api_key = api_key

'''

def gpt3(stext, engine, temp, tokens, top_p, freq_pen, pres_pen):
    openai.organization = '<<insert org>>'
    openai.api_key = '<<insert api key>>'
    response = openai.Completion.create(
        engine="davinci-instruct-beta",
        prompt=stext,
                temperature=0.3, #0-1 val; higher is more random
                max_tokens=100,  #length of response
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
        )
    content=response.choices[0].text.split('.')
    print(content)
    return response.choices[0].text


query = 'What is global warming?'

response = gpt3(query)

print(response)

'''

'''Import data'''
file_import_location = '<<local file location>>'
jokes_df  = pd.read_excel(file_import_location + 'climate_change_jokes.xlsx')

'''Convert df to jsonl'''
output = []
for ind in jokes_df.index:
    new_line = {"prompt": jokes_df['Prompt'][ind], "completion": jokes_df['Answer'][ind]}
    output.append(new_line)

with open(file_import_location + 'jokes.jsonl', 'w') as outfile:
        for i in output:
            json.dump(i, outfile)
            outfile.write('\n')




'''FIne tune a base model using new data'''

#openai api fine_tunes.create -t "C:\Users\stfinkelstein\Documents\Personal\Climate Hackathon\jokes.jsonl" -m text-davinci-002

'''Upload the file first'''
openai.File.create(
    file = open("C:\\Users\\stfinkelstein\\Documents\\Personal\\Climate Hackathon\\jokes.jsonl", "rb"),
    purpose = 'fine-tune'
    )

#"file-z0oXeFKKnviaTM2pIqKTRrKv"

'''Fine tune model'''
openai.FineTune.create(
    training_file = "file-z0oXeFKKnviaTM2pIqKTRrKv",
    model = 'davinci'
    )

fine_tuned_model = 'davinci:ft-oai-hackathon-2022-team-41-2022-11-12-22-01-38'


'text-davinci-002'

'''
#################################################################################
##############################          Start here          ###################################################
############################################################################################
'''


'''Liam's code with slight tweaks to parameters and prompts'''

'''Creating prompts for the climate change topic, image, and caption'''


'''Create lists for df later on'''
i = 0
climate_concepts = []
image_descriptions = []
image_captions = []
image_names = []
image_links = []


'''Start here'''
#climate_concepts.pop()
#image_descriptions.pop()
#image_captions.pop()

#print(len(climate_concepts))
#print(len(image_names))

concept = openai.Completion.create(
    model='text-davinci-002',
    prompt="Generate a concept related to climate change:\n",
    temperature=1,
    max_tokens=20,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0
    )

print(concept.choices[0].text)
climate_concepts.append(concept.choices[0].text.strip())

#"Describe a funny image that represents this:\n",
#concept.choices[0].text + scene.choices[0].text + "With a funny caption:\n",

scene = openai.Completion.create(
    model='text-davinci-002',
    prompt = "Describe a funny image representing this:\n" + concept.choices[0].text.strip(),
    temperature=1,
    max_tokens=30,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0
)

print(scene.choices[0].text)
image_descriptions.append(scene.choices[0].text.strip())

caption = openai.Completion.create(
    model='text-davinci-002',
    prompt = "Generate a funny caption about this:\n" + scene.choices[0].text.strip(),
    temperature=1,
    max_tokens=30,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0
    ) 
print(caption.choices[0].text)
image_captions.append(caption.choices[0].text.strip())

'''
test = 'funny Climate change refers to a broad array of environmental degradation that is predicted to'

image = openai.Image.create(prompt=test, n=1, size="1024x1024")
print(image.data[0].url)
'''

image = openai.Image.create(prompt=scene.choices[0].text.strip(), n=1, size="1024x1024")
print(image.data[0].url)
image_links.append(image.data[0].url)

image_name = caption.choices[0].text[0:10]

'''Remove special characters from image file name'''
image_name =re.sub("[^A-Z]", "", image_name,0,re.IGNORECASE)
image_name = image_name.strip()
image_name = image_name + '_' + str(i)
image_names.append(image_name)
print(image_name)
i+=1


'''Save picture manually first'''
response = requests.get(image.data[0].url)
file_name = file_import_location + 'images_generated/' + image_name + '.jpg'
if response.status_code == 200:
    with open(file_name, "wb") as f:
        f.write(response.content)
        
        
'''Open image and add caption'''
# Open an Image
temp_img = Image.open(file_name)
 
# Call draw Method to add 2D graphics in an image
I1 = ImageDraw.Draw(temp_img)
 
# Add Text to an image
fontsize = 30
font = ImageFont.truetype("arial.ttf", fontsize)
I1.text((28, 36), caption.choices[0].text , font= font, fill=(255, 0, 0))
 
# Display edited image
temp_img.show()
 
# Save the edited image
file_name_withcaption = file_import_location + 'images_generated/' + image_name + '_withcaption.jpg'
temp_img.save(file_name_withcaption)



'''Create a dataframe by zipping together all of the lists'''

list_of_tuples = list(zip(climate_concepts, image_descriptions, image_captions, image_names,image_links ))
climate_change_images_df = pd.DataFrame(list_of_tuples, columns = ['Climate_Concept', 'Image_Description', 'Image_Caption', 'Image_Filename', 'Image_Link'])
climate_change_images_df.head()




'''Export to Excel'''

#Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(file_import_location + 'climate_change_gpt3_image_data.xlsx', engine='xlsxwriter')

# Write each dataframe to a different worksheet.
climate_change_images_df.to_excel(writer, sheet_name='Image_Data', index=False)


# Close the Pandas Excel writer and output the Excel file.
writer.save()