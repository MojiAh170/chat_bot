from gtts import gTTS
import os

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("output.mp3")
    os.system("start output.mp3")  # برای ویندوز
    # os.system("mpg321 output.mp3")  # برای لینوکس
    # os.system("afplay output.mp3")  # برای مک

# تست برای زبان فارسی
text_fa = "سلام، حال شما چطور است؟"
text_to_speech(text_fa, lang='fa')
