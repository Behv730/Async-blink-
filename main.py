# toggle between two states, blinking led and led off, using a button.
# wiring can be infered from code
#
# Raspberry pi pico 
# MicroPython version: 1.23.0
# Author: Behv730
# Date: 2024.12.30
from machine import Pin
import asyncio

SUSTAIN_PRESS = 25

# Declare pins
led = Pin("LED", Pin.OUT)
button = Pin(9,Pin.IN, Pin.PULL_DOWN)

def bpm(n):
  """returns the time interval between beats, giving Beats Per Minute"""
  return 60/n

async def blink(led_pin, duration, beats, press_event):
  """Prefered input state is led_pin.off()"""
  while True:
    await press_event.wait()
    # pulse the led for duration-ms
    led_pin.on()
    await asyncio.sleep_ms(duration)
    print("blink")
    led_pin.off()
    # wait for 1 beat
    await asyncio.sleep(bpm(beats))
  
  
async def debounce(input, sustain, press_event):
  """take samples sustain ms-apart, if values match return value."""
  while True:
    # sample twice with sustain-ms appart
    state1 = input.value()
    await asyncio.sleep_ms(sustain)
    state2 = input.value()
    
    # toggle press_event
    if (state1 and state2 == 1):
      if not press_event.is_set():   
        press_event.set()
        print(f"press_event {press_event.is_set()}")
      elif press_event.is_set():
        press_event.clear()
        print(f"press_event {press_event.is_set()}")

async def main():
  press = asyncio.Event()
  asyncio.create_task(debounce(button, 80, press))
  asyncio.create_task(blink(led,30,120, press))
  await asyncio.sleep(1000) # keeps the other tasks running by making main() span 1000sec


asyncio.run(main())
