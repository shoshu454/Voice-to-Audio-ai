import sys
from PySide2.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PySide2.QtUiTools import loadUiType, QUiLoader
from PySide2.QtCore import QFile, Qt
from PySide2.QtGui import QIcon
import speech_recognition as sr
import pyttsx3
import requests
import json

class Gui(QWidget):
    def __init__(self):
        # 加载ui文件，创建qt文件对象，加载文件对象并创建ui对象
        super().__init__()
        QtFileObj = QFile("firsttime.ui")
        QtFileObj.open(QFile.ReadOnly)
        QtFileObj.close()
        self.ui = QUiLoader().load(QtFileObj)

        # # 设置界面图标
        # icon = QIcon("yk.ico")
        # self.ui.setWindowIcon(icon)

        # # 变量定义、ui组件对象属性设置
        # self.index = 0
        # self.ui.tableWidgetAnswer.horizontalHeader().setVisible(True)  # 设置tableWidget组件的标题显示为True
        self.ui.pushButton.clicked.connect(self.rename)  # 绑定按钮的方法
        self.ui.label.setText("jo")

    def rename(self):
        self.ui.label.setText("new jo")

    def logger_show(self):
        # 插入内容
        logger_item = {
            'one': '-' * 20, 'two': '-' * 20, 'three': '-' * 20, 'four': '-' * 20,
            'five': '程序已经开始运行，请勿多次点击开始运行按钮'
        }
        self.ui.tableWidgetAnswer.insertRow(int(self.ui.tableWidgetAnswer.rowCount()))
        self.index += 1
        new_item_one = QTableWidgetItem(logger_item['one'])
        new_item_one.setTextAlignment(Qt.AlignCenter)
        new_item_two = QTableWidgetItem(logger_item['two'])
        new_item_two.setTextAlignment(Qt.AlignCenter)
        new_item_three = QTableWidgetItem(logger_item['three'])
        new_item_three.setTextAlignment(Qt.AlignCenter)
        new_item_four = QTableWidgetItem(logger_item['four'])
        new_item_four.setTextAlignment(Qt.AlignCenter)
        new_item_five = QTableWidgetItem(logger_item['five'])
        new_item_five.setTextAlignment(Qt.AlignCenter)
        self.ui.tableWidgetAnswer.setItem(self.index - 1, 0, new_item_one)
        self.ui.tableWidgetAnswer.setItem(self.index - 1, 1, new_item_two)
        self.ui.tableWidgetAnswer.setItem(self.index - 1, 2, new_item_three)
        self.ui.tableWidgetAnswer.setItem(self.index - 1, 3, new_item_four)
        self.ui.tableWidgetAnswer.setItem(self.index - 1, 4, new_item_five)
        # 定位至最新行
        self.ui.tableWidgetAnswer.verticalScrollBar().setSliderPosition(self.index)
        # 刷新
        QApplication.processEvents()

def recognize_speech():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the microphone as the audio source
    with sr.Microphone() as source:

        # print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)  # Calibrates to ambient noise
        print("Listening... Speak now.")

        try:
            # Capture audio from the microphone
            audio = recognizer.listen(source)

            # Use Google's free Web Speech API
            # print("Recognizing...")
            text = recognizer.recognize_google(audio)
            # print("You said:", text)
            return text

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            print(f"API request error: {e}")
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # Speed of speech
    engine.setProperty("volume", 0.9)

    engine.say(text)
    engine.runAndWait()




def generate_text(prompt_text):
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

    payload = json.dumps({
        "model": "ep-20250111221520-5pcbg",
        "messages": [
            # {
            #     "role": "system",
            #     "content": "You are a helpful assistant."
            # },
            {
                "role": "user",
                "content": prompt_text
            }
        ]
    })
    headers = {
        'Authorization': 'Bearer 8cdebf6b-d122-402b-b703-66b6c66c5639',
        'Content-Type': 'application/json',
        'max_tokens': '50'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # message_content = response_json.get('message', {}).get('content')
    # response = {'text': ''}
    # response['text'] = {"choices":[{"finish_reason":"stop","index":0,"logprobs":'null',"message":{"content":"以下是一段描写春天景色的优美文字：\n\n春天如一幅绚丽的画卷，。","role":"assistant"}}],"created":1736777574,"id":"021736777566162e9c84b913dc3d17489c8a44078364cc12b2d4e","model":"doubao-pro-4k-240515","object":"chat.completion","usage":{"completion_tokens":220,"prompt_tokens":19,"total_tokens":239,"prompt_tokens_details":{"cached_tokens":0}}}
    response_json = response.json()
    content = response_json['choices'][0]['message']['content']
    # print(content)
    return content


if __name__ == '__main__':
    prompt = recognize_speech()
    result_text = generate_text(prompt)
    print(result_text)
    text_to_speech(result_text)
    # app = QApplication(sys.argv)
    # ykGuiObj = Gui()
    # ykGuiObj.ui.show()
    # sys.exit(app.exec_())

