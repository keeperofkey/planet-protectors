# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 14:20:22 2022

"""

import pandas as pd
import numpy as np
import openai
import os
import json

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




'''Liam's code with slight tweaks to parameters and prompts'''

'''Creating prompts for the climate change topic, image, and caption'''

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

#"Describe a funny image that represents this:\n",
#concept.choices[0].text + scene.choices[0].text + "With a funny caption:\n",

scene = openai.Completion.create(
    model='text-davinci-002',
    prompt = "Describe a funny image representing this:\n" + concept.choices[0].text,
    temperature=1,
    max_tokens=30,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0
)

print(scene.choices[0].text)

caption = openai.Completion.create(
    model='text-davinci-002',
    prompt = "Write a funny caption about this:\n" + scene.choices[0].text,
    temperature=0.7,
    max_tokens=30,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0
    ) 
print(caption.choices[0].text)

'''
test = 'funny Climate change refers to a broad array of environmental degradation that is predicted to'

image = openai.Image.create(prompt=test, n=1, size="1024x1024")
print(image.data[0].url)
'''

image = openai.Image.create(prompt=scene.choices[0].text, n=1, size="1024x1024")
print(image.data[0].url)



img_data = requests.get(image.data[0].url).content
with open("./images/{}.jpg".format(caption.choices[0].text), 'wb') as handler:
    handler.write(img_data)





'''

Next steps

automate putting caption in image

prompt engineering??? Clean up text being fed into the models.


take first split of first response....split by period/exclamation point
'''






