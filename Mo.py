from gtts import gTTS
import os

def text_to_speech(text, lang='en'):
    # تبدیل متن به صوت با استفاده از gTTS
    tts = gTTS(text=text, lang=lang, slow=False)
    # ذخیره صوت به یک فایل
    tts.save("output.mp3")
    # پخش فایل صوتی
    os.system("start output.mp3")  # برای ویندوز
    # os.system("mpg321 output.mp3")  # برای لینوکس
    # os.system("afplay output.mp3")  # برای مک

# تست برنامه برای زبان انگلیسی
text_en = "Hello, how are you?"
text_to_speech(text_en, lang='en')

# تست برنامه برای زبان فارسی
text_fa = "سلام، حال شما چطور است؟"
text_to_speech(text_fa, lang='fa')
