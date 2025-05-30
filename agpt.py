import google.generativeai as genai
import argparse
import os
import re
import configparser

parser=argparse.ArgumentParser()
#parser.add_argument("text", type=str, )
parser.add_argument("--list-models",  action="store_true")
#parser.add_argument("--q
args=parser.parse_args()

google_key="APK_KEY"

if not os.path.exists("conf.ini"):
    ans=input("No conf.ini exists. Create one (y/n) : ")
    if ans.lower()=="y" or ans.lower()=="yes":
        print("Ok.")
        with open("conf.ini", "w") as file:
            file.write(f'''[settings]
api_key = AIzaSyBFs-4wRCRNDBF9wdCZeA-810yQvMsYmZc''')
        if not os.path.exists("conf.ini"):
            print("something went wrongg.")
            exit()
        else:
            print("Done.")
    else:
        print("Ok. Using default API Key.")

try:
    config=configparser.ConfigParser()
    config.read("conf.ini")
    google_key=config.get("settings", "api_key")
except Exception as e:
    skip=True

# config the ai model

genai.configure(api_key=google_key)

if args.list_models:
    models = genai.list_models()
    for model in models:
        print(model.name)
    os._exit(0)
mapping={"*":"",}

def replace_strings(text, mapping):
    pattern=re.compile("|".join(re.escape(k) for k in mapping.keys()))
    return pattern.sub(lambda m: mapping[m.group(0)], text)

# opening print, remind that command 'quit' exits the agpt
print("AGPT Ready. '/quit' to exit")

while True:
    user_input=input(": ")
    if user_input.lower()=="/quit" or user_input.lower()=='/exit':
        print("Exiting..")
        break

    model=genai.GenerativeModel("gemini-2.5-flash-preview-04-17")
    response=model.generate_content(user_input)
    fixed_response=replace_strings(response.text, mapping)
    print(fixed_response)
