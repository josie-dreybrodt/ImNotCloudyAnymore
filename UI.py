from PyQt6.QtCore import Qt, QTimer,QPropertyAnimation, QEasingCurve, QSize,QPoint
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QGraphicsOpacityEffect
from PyQt6.QtGui import QPixmap, QMovie, QFont
from PyQt6.QtWidgets import QLabel
import sys, weather

app = QApplication(sys.argv)

class UI(QWidget):  # UI inherits from QWidget
    def __init__(self):
        super().__init__() # initialize QWidget
        self.weather = weather.Weather()
        self.weather.start_weather(on_update=self.on_data_ready)
        self.current_temp = self.weather.data["current"]["temperature_2m"]
        self.current_code = None
        self.movie = None
        self.temp = self.current_temp
        #------------- Timer for mouse events
        self.timer_m = QTimer()
        self.timer_m.timeout.connect(self.check_mouse)
        self.timer_m.start(100)  # fires every 100 ms
        #------------- Window setup
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent")
        #------------- Close-Button Config
        self.button = QPushButton(self)
        self.button.setText("✖")
        self.button.move(220, 13)
        self.button.setFixedSize(30, 30)
        self.button.setStyleSheet("background: rgba(220,0,0,150);border-radius: 10px; color: white;font-size: 15px;")
        self.button.clicked.connect(self.close)
        self.button.hide()
        #-------------- °C display
        self.temp_label = QLabel(self)
        self.temp_label.setStyleSheet("background: transparent")
        self.temp_label.setFont(QFont('Times', 12, QFont.Weight.Bold))
        self.temp_label.setText(f"{self.temp}°C")
        self.temp_label.move(110,180)
        #---------------
        self.imagelabel = QLabel(self)
        self.imagelabel.setScaledContents(True)
        self.imagelabel.setFixedSize(256, 256)
        self.weather_update()
        #-------------- Timer for updating the sprites
        timer_s = QTimer()
        timer_s.timeout.connect(self.weather_update)
        timer_s.start(60000)
        #------------- Timer for updating the temperature
        self.temp_update_timer = QTimer()
        self.temp_update_timer.timeout.connect(self.temp_update)
        self.temp_update_timer.start(30000)
        #------------- Timer for the temperature animation
        self.temp_timer = QTimer()
        self.temp_timer.timeout.connect(self.count_temp)
        self.temp_update()
        #------------- Timer for refreshing the weather data (every 2 minutes)
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.api_refresh)
        self.refresh_timer.start(2 * 60 * 1000)

        # #------------ FOR TESTING
        # self.test_codes = ["sun", "cloud", "rain", "night", "snow", "thunder", "fog"]
        # self.test_index = 0
        #
        # self.test_timer = QTimer()
        # self.test_timer.timeout.connect(self.test_switch)
        # self.test_timer.start(3000)  # switch every 3 seconds
        # #--------------------


        self.resize(350, 350)
        self.show()

        sys.exit(app.exec())

    def animation(self, new_movie_path):
        if new_movie_path is None:
            return
        # Fade-Out
        effect = QGraphicsOpacityEffect(self.imagelabel)
        self.imagelabel.setGraphicsEffect(effect)

        self.fade_out = QPropertyAnimation(effect, b"opacity")
        self.fade_out.setDuration(300)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)

        def on_fade_out_done():
            if self.movie:
                self.movie.stop()
            self.movie = QMovie(new_movie_path)
            # Stop old movie, load new one
            self.movie.stop()
            self.movie = QMovie(new_movie_path)
            self.imagelabel.setMovie(self.movie)
            self.movie.start()

            # Fade-In
            self.fade_in = QPropertyAnimation(effect, b"opacity")
            self.fade_in.setDuration(300)
            self.fade_in.setStartValue(0.0)
            self.fade_in.setEndValue(1.0)
            self.fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)
            self.fade_in.start()

        self.fade_out.finished.connect(on_fade_out_done)
        self.fade_out.start()

    def change_sprite(self):
        if self.current_code == "night":
            self.button.move(220, 13)
            self.temp_label.move(100, 220)
            return "sprite/NightSprite.gif"
        elif self.current_code == "cloud":
            self.button.move(220, 13)
            self.temp_label.move(110, 180)
            return "sprite/CloudSprite.gif"
        elif self.current_code == "sun":
            self.button.move(220, 13)
            self.temp_label.move(100,250)
            return "sprite/SunSprite.gif"
        elif self.current_code == "rain":
            self.temp_label.move(110, 11)
            self.button.move(260, 7)
            return "sprite/RainSprite.gif"
        elif self.current_code == "fog":
            self.temp_label.move(110, 11)
            self.button.move(230, 13)
            return "sprite/FogSprite.gif"
        elif self.current_code == "snow":
            self.temp_label.move(120, 10)
            self.button.move(220, 13)
            return "sprite/SnowSprite.gif"
        elif self.current_code == "thunder":
            self.temp_label.move(110, 11)
            self.button.move(220, 13)
            return "sprite/ThunderSprite.gif"

    def weather_update(self):
        new_code = self.weather.weather_code()
        #new_code = "cloud"

        if new_code != self.current_code:
            self.current_code = new_code
            path = self.change_sprite()
            self.animation(path)

    def temp_update(self):
        self.target_temp = self.weather.get_temperature()
        self.temp_timer.start(30)

    def count_temp(self):
        if self.current_temp < self.target_temp:
            self.current_temp = round(self.current_temp + 0.1,1)
        elif self.current_temp > self.target_temp:
            self.current_temp = round(self.current_temp - 0.1,1)
        else:
            self.temp_timer.stop()  # target reached
            return

        self.temp_label.setText(f"{self.current_temp}°C")

    def on_data_ready(self):
        # Called when the API thread is done
        QTimer.singleShot(0, self.weather_update)
        QTimer.singleShot(0, self.temp_update)

    def api_refresh(self):
        self.weather.refresh(on_update=self.on_data_ready)

    # #-------------- FOR TESTING
    # def test_switch(self):
    #     self.test_index = (self.test_index + 1) % len(self.test_codes)
    #     self.current_code = None  # so weather_update detects the change
    #     # set the next code directly
    #     new_code = self.test_codes[self.test_index]
    #     self.current_code = new_code
    #     path = self.change_sprite()
    #     self.animation(path)
    # #--------------------------


    def enterEvent(self, event):
        self.button.show()
        self.button.raise_()

    def check_mouse(self):
        if not self.rect().contains(self.mapFromGlobal(self.cursor().pos())):
            self.button.hide()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
        self.dragPos = event.globalPosition().toPoint()


main=UI()
