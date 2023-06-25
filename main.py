import board
import displayio
import framebufferio
import rgbmatrix
import time
import adafruit_display_text.label
import terminalio
import wifi
import os
import socketpool
import adafruit_requests
import ssl
import microcontroller
import weather_conditions
import space_ship

bit_depth_value = 6
unit_width = 64
unit_height = 64
chain_width = 1
chain_height = 1
serpentine_value = True

width_value = unit_width * chain_width
height_value = unit_height * chain_height

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=width_value, height=height_value, bit_depth=bit_depth_value,
    rgb_pins=[board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
    addr_pins=[board.GP10, board.GP16, board.GP18, board.GP20, board.GP22],
    clock_pin=board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13,
    tile=chain_height, serpentine=serpentine_value,
    doublebuffer=True
)

DISPLAY = framebufferio.FramebufferDisplay(matrix, auto_refresh=True, rotation=180)


now = t0 = time.monotonic_ns()
append_flag = 0

class RGB_Api():
    def __init__(self):
        #API Request
        self.url = "https://weatherapi-com.p.rapidapi.com/current.json?q=" + os.getenv('postcode')
        self.headers = {'X-RapidAPI-Key': os.getenv('RapidAPI-Key'), 'X-RapidAPI-Host': os.getenv('RapidAPI-Host')}
        self.timeUrl = "http://worldtimeapi.org/api/timezone/Europe/London"
        
        #Display information
        self.condition = ""
        self.temp_c = ""
        self.localtime = time.localtime()
        self.condition_array = weather_conditions.condition_images
        
        #Text
        self.txt_str = "" 
        self.txt_color = 0x306ED2
        self.txt_x = 0
        self.txt_y = 4
        self.txt_font = terminalio.FONT
        self.txt_line_spacing = 1
        self.txt_scale = 1
        
    def static_image(self, imagePath, x, y):
        bitmap1 = displayio.OnDiskBitmap(open(imagePath, 'rb'))
        
        tile_grid1 = displayio.TileGrid(
            bitmap1,
            pixel_shader=getattr(bitmap1, 'pixel_shader', displayio.ColorConverter())
        )
        
        tile_grid1.x = x
        tile_grid1.y = y
        
        return tile_grid1
    
    def static_text(self):
        TEXT = adafruit_display_text.label.Label(
            self.txt_font,
            color=self.txt_color,
            scale=self.txt_scale,
            text=self.txt_str,
            line_spacing=self.txt_line_spacing
        )
        
        TEXT.x = self.txt_x
        TEXT.y = self.txt_y
        
        return TEXT
    
    def setup_WIFI(self):
        wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
        
    def get_weather(self):
        pool = socketpool.SocketPool(wifi.radio)
        requests = adafruit_requests.Session(pool, ssl.create_default_context())
        
        try:
            response = requests.get(url=self.url, headers=self.headers)
            response_as_json = response.json()
            self.condition = response_as_json['current']['condition']['text']
            self.temp_c = int(response_as_json['current']['temp_c'])
            self.getTime()
        except Exception as e:
            print("Error:\n", str(e))
            print("Resetting microcontroller in 10 seconds")
            time.sleep(10)
            microcontroller.reset()
            
    def getTime(self):
        pool = socketpool.SocketPool(wifi.radio)
        requests = adafruit_requests.Session(pool, ssl.create_default_context())
        
        try:
            response = requests.get(url=self.timeUrl)
            response_as_json = response.json()
            
            self.localtime = time.localtime(response_as_json['unixtime']+ 3600)
        except Exception as e:
            print("Error:\n", str(e))
            
    def update_text(self):
        self.getTime()
        timestamp = time.mktime(self.localtime)  
        dateStr = "{:02d}/{:02d}/{:02d}".format(self.localtime.tm_mday, self.localtime.tm_mon, self.localtime.tm_year)
        #Time with seconds
        #timeStr = "{:02d}:{:02d}:{:02d}".format(self.localtime.tm_hour, self.localtime.tm_min, self.localtime.tm_sec)
        timeStr = "{:02d}:{:02d}".format(self.localtime.tm_hour, self.localtime.tm_min)        
        
        if (self.localtime.tm_min == 0 or
            self.localtime.tm_min == 15 or
            self.localtime.tm_min == 30 or
            self.localtime.tm_min == 45) and self.localtime.tm_sec == 0:
            self.get_weather()

        
        self.txt_str = dateStr + "\n" + timeStr + "\n" + str(self.temp_c) + 'C ' + "\n" 
if __name__ == '__main__':
    RGB = RGB_Api()
    RGB.setup_WIFI()
    RGB.get_weather()

    images = space_ship.images

    while True:
        for i in range(len(images)):
            RGB.update_text()
            
            GROUP = displayio.Group()        
            GROUP.append(RGB.static_text())
            GROUP.append(RGB.static_image(RGB.condition_array[RGB.condition], 46, 12))
            GROUP.append(RGB.static_image(images[i], 0, 32))
            
            DISPLAY.show(GROUP)
            
            time.sleep(0.5)

                                                                                  
