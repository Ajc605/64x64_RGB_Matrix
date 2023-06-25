# 64x64_RGB_Matrix
RGB Matrix powered by Raspberry Pi Pico W running Cuircuit Python to display London date and time, current weather temperature ceclies and conidtion (as pixel art) and display pixal art.
# Components
64x64 RGB matrix: https://www.waveshare.com/rgb-matrix-p3-64x64.htm<br>
Raspberry Pi Pico W: https://www.waveshare.com/raspberry-pi-pico-w.htm<br>
Power supply: https://www.waveshare.com/psu-5v-4a-5.5-2.1-us.htm<br>

# APIs
To get weather I'm using WeatherAPI (https://www.weatherapi.com/) with the postcode found in Setting.toml. From this reposne current->temp_c is displayed and the current->condition->text is used to get a pixel art from weather_conditions.py and displayed. The API is called upon starting the program and every quarter of the hour to update the temp_c and condition. This API does require a registration and is rate limited<br>

To get the current time I'm using WorldTimeAPI (http://worldtimeapi.org/), this is called in every iteration of the loop. There's not registration or rate limit for this API.

# Setup
A good beginers guide can be found here (https://www.waveshare.com/wiki/RGB-Matrix-P3-64x64#Hardware_Connection_3) and the demo is the foundation of this project.<br>

To make the API request I'm using adafruit_requests library, this requires wifi to be set up with 'CIRCUITPY_WIFI_SSID' and 'CIRCUITPY_WIFI_PASSWORD'. These can be set in settings.toml. Once an account has been made for Weather API the credentails can be set in settings.toml as well. <br>

# Main
Firstly the main set's up the RGB object, then set's up the wifi object ready for the API request. An inital weather API request is made and the pixel art images are retrieve. The program then starts an inifint loop, which loops over each image file. On each iteration an API call is done to get the time and the next image.

# Pixel Art
Using Pixilart (https://www.pixilart.com) to create 64x32 .bmp files, storing these in a pixalArt/../ and creating a specify pythony filer with an array of all images to loop over. space_ship.py is an example of this. Within the main.py we can set images (line 142) to the file which contains the images to display. <br>
My processs to create .bmp files has been to create the image on Pixilart, download this as .png and using GIMP (https://www.gimp.org/) to exporty as .bmp. 

# Additonal Notes
I have been using Thonny (https://thonny.org/) to program the Raspberry Pi.

