from PyQt6.QtCore import Qt, QTimer,QPropertyAnimation, QEasingCurve, QSize,QPoint
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QGraphicsOpacityEffect
from PyQt6.QtGui import QPixmap, QMovie, QFont
from PyQt6.QtWidgets import QLabel
import sys, Main

app = QApplication(sys.argv)

class UI(QWidget):  #UI erbt von QWidget
    def __init__(self):
        super().__init__()# QWidget initialisieren
        self.wetter = Main.Weather()
        self.wetter.start_weather(on_update=self.on_data_ready)
        self.current_temp = self.wetter.data["current"]["temperature_2m"]
        self.current_code = None
        self.movie = None
        self.temp = self.current_temp
        #------------- Timer für Mausevent
        self.timer_m = QTimer()
        self.timer_m.timeout.connect(self.maus_pruefen)
        self.timer_m.start(100)  # alle 100ms klingeln
        #------------- Parent-Fenster anpassung
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
        #--------------°C Anzeige
        self.gradcelsius = QLabel(self)
        self.gradcelsius.setStyleSheet("background: transparent")
        self.gradcelsius.setFont(QFont('Times', 12, QFont.Weight.Bold))
        self.gradcelsius.setText(f"{self.temp}°C")
        self.gradcelsius.move(110,180)
        #---------------
        self.imagelabel = QLabel(self)
        self.imagelabel.setScaledContents(True)
        self.imagelabel.setFixedSize(256, 256)
        self.weather_update()
        #-------------- Timer zum aktualisieren der Sprites
        timer_s = QTimer()
        timer_s.timeout.connect(self.weather_update)
        timer_s.start(60000)
        #------------- Timer zum aktualisieren der Temperatur
        self.temp_update_timer = QTimer()
        self.temp_update_timer.timeout.connect(self.temp_update)
        self.temp_update_timer.start(30000)
        #------------- Timer zum aktualisieren der Temperaturanimation
        self.temp_timer = QTimer()
        self.temp_timer.timeout.connect(self.count_temp)
        self.temp_update()
        #------------- 30 Minuten Timer zur aktualisierung
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.api_refresh)
        self.refresh_timer.start(2 * 60 * 1000)

        # #------------ ZUM TESTEN
        # self.test_codes = ["sun", "cloud", "rain", "night", "snow", "thunder", "fog"]
        # self.test_index = 0
        #
        # self.test_timer = QTimer()
        # self.test_timer.timeout.connect(self.test_switch)
        # self.test_timer.start(3000)  # alle 3 Sekunden wechseln
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
            # Altes Movie stoppen, neues laden
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
            self.gradcelsius.move(100, 220)
            return "sprite/NightSprite.gif"
        elif self.current_code == "cloud":
            self.button.move(220, 13)
            self.gradcelsius.move(110, 180)
            return "sprite/CloudSprite.gif"
        elif self.current_code == "sun":
            self.button.move(220, 13)
            self.gradcelsius.move(100,250)
            return "sprite/SunSprite.gif"
        elif self.current_code == "rain":
            self.gradcelsius.move(110, 11)
            self.button.move(260, 7)
            return "sprite/RainSprite.gif"
        elif self.current_code == "fog":
            self.gradcelsius.move(110, 11)
            self.button.move(230, 13)
            return "sprite/FogSprite.gif"
        elif self.current_code == "snow":
            self.gradcelsius.move(120, 10)
            self.button.move(220, 13)
            return "sprite/SnowSprite.gif"
        elif self.current_code == "thunder":
            self.gradcelsius.move(110, 11)
            self.button.move(220, 13)
            return "sprite/ThunderSprite.gif"

    def weather_update(self):
        new_code = self.wetter.weather_code()
        #new_code = "cloud"

        if new_code != self.current_code:
            self.current_code = new_code
            path = self.change_sprite()
            self.animation(path)

    def temp_update(self):
        self.target_temp = self.wetter.get_temperature()
        self.temp_timer.start(30)

    def count_temp(self):
        if self.current_temp < self.target_temp:
            self.current_temp = round(self.current_temp + 0.1,1)
        elif self.current_temp > self.target_temp:
            self.current_temp = round(self.current_temp - 0.1,1)
        else:
            self.temp_timer.stop()  # Ziel erreicht
            return

        self.gradcelsius.setText(f"{self.current_temp}°C")

    def on_data_ready(self):
        #Wenn API-Thread fertig ist
        QTimer.singleShot(0, self.weather_update)
        QTimer.singleShot(0, self.temp_update)

    def api_refresh(self):
        self.wetter.refresh(on_update=self.on_data_ready)

    # #--------------ZUM TESTEN
    # def test_switch(self):
    #     self.test_index = (self.test_index + 1) % len(self.test_codes)
    #     self.current_code = None  # damit weather_update den Wechsel erkennt
    #     # direkt den nächsten Code setzen
    #     new_code = self.test_codes[self.test_index]
    #     self.current_code = new_code
    #     path = self.change_sprite()
    #     self.animation(path)
    # #--------------------------


    def enterEvent(self, event):
        self.button.show()
        self.button.raise_()

    def maus_pruefen(self):
        if not self.rect().contains(self.mapFromGlobal(self.cursor().pos())):
            self.button.hide()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
        self.dragPos = event.globalPosition().toPoint()


main=UI()
