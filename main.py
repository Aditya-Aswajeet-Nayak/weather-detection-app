import sys
import requests
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QWidget, 
                             QLabel, QPushButton , QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.city_label = QLabel("Enter City Name:",self)
        self.city_input = QLineEdit()
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setMinimumSize(500, 600)

        #self.resize(400, 300)
        vbox = QVBoxLayout()
        self.city_input.setMinimumHeight(45)
        self.get_weather_button.setMinimumHeight(45)
        vbox.setSpacing(20)
        vbox.setContentsMargins(30, 30, 30, 30)

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.get_weather_button.clicked.connect(self.get_weather)
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        with open("style.css", "r") as file:
            self.setStyleSheet(file.read())
    def get_weather(self):
        api_key = "c2d87deb571aece440b564e73ca060e6"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()  
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_err:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request\nPlease check the city name and try again.")
                case 401:
                    self.display_error("Unauthorized\nInvalid API key.")
                case 403:
                    self.display_error("Forbidden\nAccess is denied.")
                case 404:
                    self.display_error("Not Found\nCity Not Found.")
                case 500:
                    self.display_error("Internal Server Error\nPlease try again later.")
                case 502:
                    self.display_error("Bad Gateway\nInvalid response from the server.")
                case 503:
                    self.display_error("Service Unavailable\nServer is down.")
                case 504:
                    self.display_error("Gateway Timeout\nNo response from the server.")
                case _:
                    self.display_error(f"HTTP Error occurred\n{http_err}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nPlease check your internet connection and try again.")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error\nThe request timed out. Please try again later.")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects\nThe request was redirected too many times.")                    
                
        except requests.exceptions.RequestException as req_error:
            print(f"An error occurred: {req_error}")

    
    def display_error(self, message):
        self.temperature_label.setStyleSheet("color: red; font-size: 25px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        temp_k = data["main"]["temp"]
        temp_c = temp_k - 273.15
        temp_f = (temp_k *9/5) - 459.67
        weather_id = data["weather"][0]["id"]
        self.temperature_label.setStyleSheet("color: white; font-size: 25px;")
        weather_description = data["weather"][0]["description"]
        self.temperature_label.setText(f"Temperature: {temp_c:.2f}°C / {temp_f:.2f}°F")
        self.emoji_label.setStyleSheet("font-size: 50px;")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setStyleSheet("color: white; font-size: 25px;")

        self.description_label.setText(weather_description)
    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id < 232:
            return "⛈️"  # Thunderstorm
        elif 300 <= weather_id < 321:
            return "🌧️"  # Drizzle
        elif 500 <= weather_id < 531:
            return "🌧️"  # Rain
        elif 600 <= weather_id < 622:
            return "❄️"  # Snow
        elif 700 <= weather_id < 741:
            return "🌫️"  # Atmosphere (fog, mist, etc.)
        elif weather_id == 762:
            return "🌋"  # Volcanic ash
        elif weather_id == 771:
            return "🌬️"  # Wind
        elif weather_id == 781:
            return "🌪️"  # Tornado
        elif weather_id == 800:
            return "☀️"  # Clear sky
        elif 801 <= weather_id < 900:
            return "☁️"  # Clouds
        else:
            return "❓"  # Unknown weather condition
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())        
