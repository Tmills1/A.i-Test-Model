
import os
import pyaudio
import speech_recognition as sr
import playsound
from gtts import gTTS
import requests
import uuid
import ipinfo
import openai

# Replace with your IPInfo access token
ipinfo_access_token = "0a54859de9430a"

# Replace with your VirusTotal API key
virustotal_api_key = "4b8c004939844bbceb56033f08d0accbc1eab4f8062c1f1d8a16c81d5281283b"

# Replace with your OpenAI API key
openai.api_key = "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"

lang = 'en'

guy = ""

def convert_spoken_ip(spoken_ip):
    converted_ip = spoken_ip.replace("dot", ".").replace(" ", "")
    return converted_ip

def get_command_and_argument(said):
    words = said.split()
    command = words[0]
    argument = ' '.join(words[1:])
    return command, argument

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        print("Listening...")
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print("Recognized text:", said)
            global guy
            guy = said

            if "Friday" in said:
                command, argument = get_command_and_argument(said)
                print("Command:", command)
                print("Argument:", argument)
                if command == "scan":
                    process_scan_command(argument)
                else:
                    response_text = get_openai_response(said)
                    speak_response(response_text)

        except Exception as e:
            print("Exception:", e)

        return said

def get_user_input():
    user_input = input("Enter a command or value: ")
    return user_input

def process_scan_command(argument):
    if "IP address" in argument:
        ip_address = argument.replace("IP address", "").strip()
        converted_ip = convert_spoken_ip(ip_address)
        search_ipinfo(converted_ip)
    elif "file" in argument:
        # Perform VirusTotal file scan here
        pass
    elif "URL" in argument:
        # Perform VirusTotal URL scan here
        pass

def get_openai_response(prompt):
    completion = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50
    )
    return completion.choices[0].text.strip()

def search_ipinfo(ip_address):
    handler = ipinfo.getHandler(ipinfo_access_token)
    details = handler.getDetails(ip_address)
    print("IPInfo API Result:", details.all)

def speak_response(text):
    speech = gTTS(text=text, lang=lang, slow=False, tld="com.au")
    file_name = f"response_{str(uuid.uuid4())}.mp3"
    speech.save(file_name)
    playsound.playsound(file_name, True)

def main():
    while True:
        choice = input("Enter 'voice' for voice recognition or 'text' for manual input: ")
        
        if choice == 'voice':
            get_audio()
        elif choice == 'text':
            user_input = get_user_input()
            if "Friday" in user_input:
                command, argument = get_command_and_argument(user_input)
                if command == "scan":
                    process_scan_command(argument)
                else:
                    response_text = get_openai_response(user_input)
                    print(response_text)
        elif choice == 'stop':
            break
        else:
            print("Invalid choice. Please enter 'voice', 'text', or 'stop'.")

if __name__ == "__main__":
    main()
