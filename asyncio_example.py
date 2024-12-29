# Virkar, micropython v1.23.0, latest at the time. not the same one in opt/homebrew/bin/
# https://docs.micropython.org/en/v1.23.0/library/asyncio.html#asyncio.Loop

import asyncio
from machine import Pin

async def blink(led, period_ms):
    while True:
        led.on()
        await asyncio.sleep_ms(5)
        led.off()
        await asyncio.sleep_ms(period_ms) # type: ignore

async def main(led1, led2):
    asyncio.create_task(blink(led1, 700))
    asyncio.create_task(blink(led2, 400))
    await asyncio.sleep_ms(10_000)


# Running on a generic board
onboard_led = Pin("LED", Pin.OUT)
ext_led = Pin(4,Pin.OUT)

asyncio.run(main(onboard_led, ext_led))