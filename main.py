"""láta takka toggla milli tvegja ástanda, blikka og off."""
from machine import Pin
import asyncio

SUSTAIN = 60

# Declare pins
led = Pin("LED", Pin.OUT)
button = Pin(9,Pin.IN, Pin.PULL_DOWN)

def bpm(n):
  """returns the interval between the number of beats inputed"""
  return 60/n

async def pulse(led_pin, duration):
  """prefered input state is led_pin.off()"""
  led_pin.on()
  await asyncio.sleep_ms(duration)
  led_pin.off()
  
  
async def debounce(input, sustain):
  """take samples sustain ms apart, if values match return value."""
  while True:
    state1 = input.value()
    await asyncio.sleep_ms(sustain)
    state2 = input.value()
    if state1 and state2 == 1:
      print(f"debounce = {state1}{state2}")
      # led.toggle() # for testing
      return 1

async def debounce_test():
  task1 = asyncio.create_task(debounce(button, SUSTAIN))
  while True:
    # await task1
    if await debounce(button, SUSTAIN):
      led.toggle()
    

press = asyncio.create_task(debounce(button, SUSTAIN))
async def main():
  while True: # main loop
    # toggle between 2 states, blink/pulse and off
    if await press:
      while True:
        await pulse(led_pin=led, duration=30)  
        await asyncio.sleep(bpm(180))
        if await press:
          break
    else:
      while True:
        led.off()
        if await press:
          break

asyncio.create_task(main())
asyncio.run(main(), press)