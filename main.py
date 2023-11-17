import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QProgressBar,
)
import cv2
import os


class VideoLabelingTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 버튼 생성 및 설정
        self.button = QPushButton("Open Video", self)
        self.button.clicked.connect(self.openFileNameDialog)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

        # 윈도우 설정
        self.setWindowTitle("Video Labeling Tool")
        self.setGeometry(300, 300, 300, 200)

        # 프로그레스바 추가
        self.progressBar = QProgressBar(self)
        layout.addWidget(self.progressBar)

    def openFileNameDialog(self):
        # 파일 선택 다이얼로그
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Select Video File", "", "Video Files (*.mp4 *.avi)", options=options
        )
        if fileName:
            self.splitAndSaveVideo(fileName)

    def splitAndSaveVideo(self, videoPath):
        # 영상을 100ms 간격으로 분할하고 저장
        cap = cv2.VideoCapture(videoPath)
        if not cap.isOpened():
            print("Error opening video file")
            return

        # 파일명 기반으로 디렉토리 생성
        baseName = os.path.splitext(os.path.basename(videoPath))[0]
        directory = os.path.join(os.path.dirname(videoPath), baseName)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # 영상 처리
        frameRate = cap.get(cv2.CAP_PROP_FPS)
        # interval = int(frameRate / 10)  # 100ms 간격
        interval = int(frameRate)  # 1000ms 간격
        frameCount = 0
        processedFrameCount = 0

        totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        expectedProcessedFrames = totalFrames // interval
        self.progressBar.setMaximum(expectedProcessedFrames)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frameCount % interval == 0:
                framePath = os.path.join(directory, f"frame_{frameCount}.jpg")
                cv2.imwrite(framePath, frame)

            processedFrameCount += 1

            self.progressBar.setValue(processedFrameCount)
            QApplication.processEvents()
            frameCount += 1

        cap.release()


# QApplication 인스턴스 생성 및 실행
app = QApplication(sys.argv)
ex = VideoLabelingTool()
ex.show()
sys.exit(app.exec_())
