import machine

## Display pins ##################################

display_pwr_pin = machine.Pin(22, machine.Pin.OUT) # IO22 Active = 0

# The oled display is connected on SPI BUS, without miso signal
sck_pin = machine.Pin(17, mode = machine.Pin.OUT)  # IO17
mosi_pin = machine.Pin(16, mode = machine.Pin.OUT) # IO16
# IO18 for esp32 module, this pin remapped on display driver as CS
miso_pin = machine.Pin(39, mode = machine.Pin.IN)
dc_pin = machine.Pin(21)   # IO21
res_pin = machine.Pin(19)  # IO19
cs_pin = machine.Pin(18)   # IO18

## Buttons pins ##################################
user_btn_pin = machine.Pin(12, machine.Pin.IN)  #IO12 Pressed = 1
enc_a_pin = machine.Pin(26, machine.Pin.IN)     #IO26 Active = 0
enc_b_pin = machine.Pin(35, machine.Pin.IN)     #IO25 Active = 0
enc_btn_pin = machine.Pin(25, machine.Pin.IN)   #IO35 Active = 0

## Devices pins ##################################
viber_pin = machine.Pin(5, mode = machine.Pin.OUT)      # IO5
buzzer_pin = machine.Pin(27, mode = machine.Pin.OUT)    # IO27
press_int_pin = machine.Pin(13, mode = machine.Pin.OUT) # IO13
acc_int_pin = machine.Pin(14, mode = machine.Pin.OUT)   # IO14

scl_pin = machine.Pin(2) # IO23
sda_pin = machine.Pin(4) # IO4

## ADC pins ##################################
#For now we leave always on
#batt_meas_en_pin = machine.Pin(39, mode = machine.Pin.OUT) #IO39 Active = 0
batt_volt_pin = machine.Pin(39) #IO39 Active = 0
