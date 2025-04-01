import sys
import pyttsx3
import queue
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QScrollArea, QGridLayout
)
from PyQt5.QtGui import QFont


class TextToSpeechApp(QWidget):
    def __init__(self):
        super().__init__()

        # 큐와 스레드로 TTS 제어
        self.tts_queue = queue.Queue()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)
        self.engine.setProperty('volume', 1.0)

        # TTS 전용 스레드 시작
        self.tts_thread = threading.Thread(target=self.process_tts_queue, daemon=True)
        self.tts_thread.start()

        # 단어 리스트
        self.words = [
            "네", "아니요", "감사합니다", "물 주세요", 
            "다리 세워주세요", "다리 눕혀 주세요", "다리 주물러주세요", "팔 주물러주세요",
            "등이 아파요", "등에 땀 닦아주세요", "전화기 주세요", "남편한테 연락해서 오라고 해주세요",
            "기저귀 갈아주세요"
        ]

        self.initUI()

    def initUI(self):
        self.setWindowTitle("오프라인 음성 출력")
        self.setGeometry(10, 100, 1800, 1200)

        main_layout = QVBoxLayout()

        self.label = QLabel("아래 버튼을 클릭하면 해당 단어를 오프라인 음성으로 출력합니다.")
        self.label.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(self.label)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        grid_layout = QGridLayout(scroll_content)
        grid_layout.setSpacing(10)

        for index, word in enumerate(self.words):
            row = index // 4
            col = index % 4
            button = QPushButton(word, self)
            button.setFixedSize(400, 200)
            button.setFont(QFont("Arial", 20, QFont.Bold))
            button.clicked.connect(lambda checked, w=word: self.speak_word(w))
            grid_layout.addWidget(button, row, col)

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def speak_word(self, word):
        self.tts_queue.put(word)

    def process_tts_queue(self):
        while True:
            word = self.tts_queue.get()
            if word:
                self.engine.say(word)
                self.engine.runAndWait()
            self.tts_queue.task_done()


# 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextToSpeechApp()
    window.show()
    sys.exit(app.exec_())
