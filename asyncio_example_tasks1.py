# https://docs.python.org/3/library/asyncio-task.html#coroutine
import asyncio
import time

######## Coroutines
# skilgr með await/async keywordinu
async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main1():
    print(f"started at {time.localtime()}")

    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.localtime()}")

# hérna telja þeir fyrstu secunduna saman, eru basicly paralell
async def main2():
  task1 = asyncio.create_task(say_after(1,'hello'))
  task2 = asyncio.create_task(say_after(2,'world'))
  
  print(f"started at {time.localtime()}")
  await task1
  await task2
  print(f"finished at {time.localtime()}")
  
#########
# corutine, notum í main_nested corutine. þessvegna heitir þetta nested
async def nested():
  return 42

async def main_nested():
  # ekkert gerist
  # þurfum að awaita corutineið svo það virki, veit ekki afh
  
  #nested()
  print(await nested())
  
# tasks schedula coroutines concurrently (simulataniosly / parallel)

async def main_nested2():
  task = asyncio.create_task(nested())
  await task

####### Futures
# sér low level awaitable obj sem táknar komandi(eventual) niðurstöðu úr async aðgerð
# þegar Future er awaituð mun coroutineð bíða eftir niðurstöðum Future annars staðar í kóðanum
# erum ekki mikið að nota það í high-level kóða (python haha)

###### sleep()
# virkar ekki get_runnuing_loop() er ekki í micropython
async def main_sleep():
  loop = asyncio.get_running_loop()
  end_time = loop.time() + 5.0
  
  while True:
      print(time.time())
      if (loop.time() + 1.0) >= end_time:
          break
      await asyncio.sleep(1)
        
async def waiter(event):
	print('waiting for it ...')
	await event.wait()
	print('... go for it')

async def main_waiter():
	event = asyncio.Event()
	# spawna taskið
	waiter_task = asyncio.create_task(waiter(event))
	# bíða í 10sec og setja svo eventið
	await asyncio.sleep(2)
	event.set()
	# bíða eftir því að waiter taskið er búið
	await waiter_task

asyncio.run(main_waiter())
# asyncio.run(main2())