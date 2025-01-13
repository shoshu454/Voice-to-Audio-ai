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
        while 1:
            print("Adjusting for ambient noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source)  # Calibrates to ambient noise
            print("Listening... Speak now.")

            try:
                # Capture audio from the microphone
                audio = recognizer.listen(source)

                # Use Google's free Web Speech API
                print("Recognizing...")
                text = recognizer.recognize_google(audio, language="zh-CN")
                print("You said:", text)

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
    # 火山引擎API的端点地址，这里需要替换为真实有效的地址
    url = input("url")

    payload = json.dumps({
        "model": input("model"),
        "stream": True,
        "messages": [
            {
                "role": "system",
                "content": prompt_text
            }
        ]

    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': input("Author")
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            result = response.json()
            return result.get('generated_text', '')  # 假设返回结果中生成文字在这个字段下，按实际改
        else:
            return f"请求失败，状态码: {response.status_code}，错误信息: {response.text}"
    except requests.RequestException as e:
        return f"请求发生异常: {str(e)}"




    # 你的Access Key
    # access_key = "AKLTYThiZTFkOTViMTI5NDQ2NjllOWE5MmUwMzU2ZTc3Mzg"
    # # 你的Secret Key
    # secret_key = "WVdReU9EQTJPRFEyTldKbE5EQm1Nemt6WkdVeFlUUTVaR1prTmpObVpXSQ=="
    # # 构建认证头信息，具体格式需按实际要求来，此处为示例
    # auth_header = f"Bearer {access_key}:{secret_key}"
    # headers = {
    #     "Authorization": auth_header,
    #     "Content-Type": "application/json"  # 假设请求体要求为JSON格式
    # }
    # # 请求体数据，根据API要求构造，这里假设包含常见的参数如模型、输入提示、生成长度等，需按实际调整
    # request_data = {
    #     "model": "ep-20250111221520-5pcbg",
    #     "prompt": prompt_text,
    #     "max_tokens": 50  # 假设生成的最大字符数，按实际需求改
    # }
    # try:
    #     response = requests.post(api_url, headers=headers, json=request_data)
    #     if response.status_code == 200:
    #         result = response.json()
    #         return result.get('generated_text', '')  # 假设返回结果中生成文字在这个字段下，按实际改
    #     else:
    #         return f"请求失败，状态码: {response.status_code}，错误信息: {response.text}"
    # except requests.RequestException as e:
    #     return f"请求发生异常: {str(e)}"
if __name__ == '__main__':
    prompt = "请帮我写一段描写春天景色的优美文字"
    result_text = generate_text(prompt)
    print(result_text)
    # text = input("Enter the text you want to convert to speech: ")
    text_to_speech(result_text)
    # recognize_speech()
    # app = QApplication(sys.argv)
    # ykGuiObj = Gui()
    # ykGuiObj.ui.show()
    # sys.exit(app.exec_())

