"""láta takka toggla milli tvegja ástanda, blikka og off."""
from machine import Pin
import asyncio

SUSTAIN = 70

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
  
  
# debounce
async def debounce(input, sustain):
  # mögulega wrappa í while true?
  state1 = input.value()
  # exit if button is off
  # while True:
    # if state1 == 0:
    #   print("exited with state1 == 0")
    #   return 0
    
  await asyncio.sleep_ms(sustain)
  state2 = input.value()
  if state1 == state2:
    print("-------------------")
    print(f"state1 = {state1}")
    print(f"state2 = {state2}")
    # led.toggle() # for testing
    return state1

async def debounce_test():
  task1 = asyncio.create_task(debounce(button, SUSTAIN))
  while True:
    # await task1
    if await debounce(button, SUSTAIN):
      led.toggle()
    


async def main():
  while True:
    await pulse(led_pin=led, duration=30)
    await asyncio.sleep(bpm(180))
#main()

asyncio.run(debounce_test())