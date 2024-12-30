"""láta takka toggla milli tvegja ástanda, blikka og off."""
import asyncio.event
from machine import Pin
import asyncio

SUSTAIN = 60

# Declare pins
led = Pin("LED", Pin.OUT)
button = Pin(9,Pin.IN, Pin.PULL_DOWN)

def bpm(n):
  """returns the interval between the number of beats inputed"""
  return 60/n

async def blink(led_pin, duration, beats, press_event):
  """prefered input state is led_pin.off()"""
  while True:
    # print("blink outer loop")
    # await asyncio.sleep_(1)
    if press_event.is_set():
      led_pin.on()
      await asyncio.sleep_ms(duration)
      print("blink")
      led_pin.off()
      await asyncio.sleep(bpm(beats))
    await asyncio.sleep_ms(5)
  
  
async def debounce(input, sustain, press_event):
  """take samples sustain ms apart, if values match return value."""
  while True:
    # sample with sustain-ms appart
    state1 = input.value()
    await asyncio.sleep_ms(sustain)
    state2 = input.value()
    print("debounce outer loop")
    #toggle press_event
    if (state1 and state2 == 1):
      if not press_event.is_set():   
        print(f"press_event {press_event.is_set()}")
        press_event.set()
      elif press_event.is_set():
        print(f"press_event {press_event.is_set()}")
        press_event.clear()

async def main():
  press = asyncio.Event()
  asyncio.create_task(debounce(button, 80, press))
  asyncio.create_task(blink(led,30,120, press))
  await asyncio.sleep(1000)


asyncio.run(main())
