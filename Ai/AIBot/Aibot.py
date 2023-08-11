import openai
import pyttsx3
import speech_recognition as spr
import sys


conversation = ''
user_name = 'George'
bot_name = 'G-one'
openai.api_key = 'აქ შეიყვანე შენი აპი ქეი.'

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

r = spr.Recognizer()
mic = spr.Microphone(device_index=1)
# print(spr.Microphone.list_microphone_names())
while True:
    with mic as source:

        print('\n' + bot_name + ' listening..')

        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print(bot_name + ' not listening..\n')

    try:
        user_input = r.recognize_google(audio)
    except:
        continue

    prompt = user_name + ":" + user_input + "\n" + bot_name + ":"
    conversation += prompt

    response = openai.Completion.create(engine='text-davinci-003', prompt=conversation, max_tokens=100)
    response_string = response["choices"][0]["text"].replace("\n", "")
    response_string = response_string.split(user_name + ": ", 1)[0].split(bot_name + ": ", 1)[0]
    conversation += response_string + "\n"
    print(response_string)
    # პასუხის(AI response-ის) აუდიო კონვერტირება.
    engine.say(response_string)
    engine.runAndWait()
    # ციკლიდან გამოსვლა თუ ჩატში სიტყვა Exit დაფიქსირდა.
    if 'exit' in user_input:
        sys.exit()
