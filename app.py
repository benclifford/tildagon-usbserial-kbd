import asyncio
import sys

from app import App
import events.keyboard as k
from events.input import ButtonDownEvent, ButtonUpEvent
from system.eventbus import eventbus


class USBSerialKeyboardApp(App):

  def __init__(self):
    print("USBSerialKeyboardApp: starting")

  async def run(self, render_update):
    print("USBSerialKeyboardApp: run")
    self.t = asyncio.create_task(self.body())
    self.minimise()

  async def body(self):
    sr = asyncio.StreamReader(sys.stdin)
    while True:
      s = await sr.read(1)
      s = s.upper()
      print(f"Read: {s!r}")
      if s in k.letters:
        e = k.letters[s]
        await eventbus.emit_async(ButtonDownEvent(e))
        await eventbus.emit_async(ButtonUpEvent(e))
        print(f"emitted letter: {e}")
      elif s in k.numbers:
        await eventbus.emit_async(k.numbers[s])
        print("emitted number")
      elif s in k.symbols:
        await eventbus.emit_async(k.symbols[s])
        print("emitted symbol")
      else:
        print("unknown key")


__app_export__ = USBSerialKeyboardApp
