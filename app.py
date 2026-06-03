import asyncio
import sys

from app import App
import events.keyboard as k
from events.input import ButtonDownEvent, ButtonUpEvent
from system.eventbus import eventbus


class USBSerialKeyboardApp(App):

  def __init__(self):
    print("USBSerialKeyboardApp: starting")
    super().__init__()

  async def run(self, render_update):
    print("USBSerialKeyboardApp: run")
    while True:
        print("Minimising")
        await render_update()
        self.minimise()
        print("... sleeping")
        await asyncio.sleep(0.05)  # yield to scheduler
        # ... which should stop this thread until
        # the next time we are accidentally
        # foregrounded.

  async def background_task(self):
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
        e = k.numbers[s]
        await eventbus.emit_async(ButtonDownEvent(e))
        await eventbus.emit_async(ButtonUpEvent(e))
        print("emitted number")
      elif s in k.symbols:
        e = k.symbols[s]
        await eventbus.emit_async(ButtonDownEvent(e))
        await eventbus.emit_async(ButtonUpEvent(e))
        print("emitted symbol")
      elif s == '\n':
        e = k.modifiers['ENTER']
        await eventbus.emit_async(ButtonDownEvent(e))
        await eventbus.emit_async(ButtonUpEvent(e))
      elif s == '\t':
        e = k.modifiers['ESCAPE']
        await eventbus.emit_async(ButtonDownEvent(e))
        await eventbus.emit_async(ButtonUpEvent(e))
      elif s == '\x1b':
        print("begin control sequence")
        s = await sr.read(1)
        if s == '[':
          print("recognised next step in control sequence")
          print("reading next step")
          s = await sr.read(1)
          if s == 'A':
            e = k.modifiers['UP']
            await eventbus.emit_async(ButtonDownEvent(e))
            await eventbus.emit_async(ButtonUpEvent(e))
          elif s == 'B':
            e = k.modifiers['DOWN']
            await eventbus.emit_async(ButtonDownEvent(e))
            await eventbus.emit_async(ButtonUpEvent(e))
          elif s == 'C':
            e = k.modifiers['RIGHT']
            await eventbus.emit_async(ButtonDownEvent(e))
            await eventbus.emit_async(ButtonUpEvent(e))
          elif s == 'D':
            e = k.modifiers['LEFT']
            await eventbus.emit_async(ButtonDownEvent(e))
            await eventbus.emit_async(ButtonUpEvent(e))
        else:
          print("unknown ESCape. probably generating mess.")
        
      else:
        print("unknown key")


__app_export__ = USBSerialKeyboardApp
