# -*- coding: utf-8 -*-
# Weather App - All functionality in a single file

from PyQt5 import QtCore, QtGui, QtWidgets
import requests

API_KEY = "82086ba43649a543517eeb92b0e2549e"  # ✅ Replace with your valid API key

class Ui_Window(object):
    def setupUi(self, Window):
        Window.setObjectName("Window")
        Window.resize(600, 455)
        self.centralwidget = QtWidgets.QWidget(Window)
        self.centralwidget.setObjectName("centralwidget")

        self.lineEdit_city = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_city.setGeometry(QtCore.QRect(0, 20, 600, 75))
        self.lineEdit_city.setPlaceholderText("Enter city name")
        self.lineEdit_city.setClearButtonEnabled(True)
        self.lineEdit_city.setObjectName("lineEdit_city")

        self.button_refresh = QtWidgets.QPushButton(self.centralwidget)
        self.button_refresh.setGeometry(QtCore.QRect(230, 310, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.button_refresh.setFont(font)
        self.button_refresh.setObjectName("button_refresh")

        self.label_current_weather = QtWidgets.QLabel(self.centralwidget)
        self.label_current_weather.setGeometry(QtCore.QRect(0, 100, 600, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_current_weather.setFont(font)
        self.label_current_weather.setFrameShape(QtWidgets.QFrame.Box)
        self.label_current_weather.setLineWidth(2)
        self.label_current_weather.setAlignment(QtCore.Qt.AlignCenter)
        self.label_current_weather.setObjectName("label_current_weather")

        self.label_forecast = QtWidgets.QLabel(self.centralwidget)
        self.label_forecast.setGeometry(QtCore.QRect(0, 160, 600, 130))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_forecast.setFont(font)
        self.label_forecast.setFrameShape(QtWidgets.QFrame.Box)
        self.label_forecast.setLineWidth(2)
        self.label_forecast.setScaledContents(False)
        self.label_forecast.setAlignment(QtCore.Qt.AlignTop)
        self.label_forecast.setWordWrap(True)
        self.label_forecast.setObjectName("label_forecast")

        Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 26))
        self.menubar.setObjectName("menubar")
        Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Window)
        self.statusbar.setObjectName("statusbar")
        Window.setStatusBar(self.statusbar)

        self.retranslateUi(Window)
        QtCore.QMetaObject.connectSlotsByName(Window)

        # 👉 Connect the button to function
        self.button_refresh.clicked.connect(self.get_weather_data)

    def retranslateUi(self, Window):
        _translate = QtCore.QCoreApplication.translate
        Window.setWindowTitle(_translate("Window", "Weather App"))
        self.button_refresh.setText(_translate("Window", "Refresh"))
        self.label_current_weather.setText(_translate("Window", "Current Weather:"))
        self.label_forecast.setText(_translate("Window", "Forecast:"))

    def get_weather_data(self):
        city = self.lineEdit_city.text().strip()
        if not city:
            self.label_current_weather.setText("Please enter a city name.")
            self.label_forecast.setText("")
            return

        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()
            print("API Response:", data)  # For debugging in terminal

            # Check for errors
            if str(data.get("cod")) != "200":
                error_message = data.get("message", "Unknown error")
                self.label_current_weather.setText(f"Error: {error_message}")
                self.label_forecast.setText("")
                return

            # Extract weather data
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"].capitalize()
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            current_weather = (
                f"City: {city}\n"
                f"Temperature: {temp}°C\n"
                f"Condition: {description}\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} m/s"
            )
            self.label_current_weather.setText(current_weather)

            # Forecast not available in free API
            self.label_forecast.setText("Forecast: Not available in free API.\nUse OneCall API for daily/hourly forecast.")

        except Exception as e:
            self.label_current_weather.setText("Error fetching data.")
            self.label_forecast.setText(str(e))


# To run the app directly from this file
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
