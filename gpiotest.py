import gpiozero
from signal import pause

btn1 = gpiozero.Button(8)
btn1.when_pressed = lambda: print("btn1 pressed")
btn2 = gpiozero.Button(7)
btn2.when_pressed = lambda: print("btn2 pressed")

rot_up = gpiozero.Button(10)
rot_up.when_pressed = lambda: print("rotary up")
rot_down = gpiozero.Button(9)
rot_down.when_pressed = lambda: print("rotary down")
rot_click = gpiozero.Button(25)
rot_click.when_pressed = lambda: print("rotary click")

print("Running GPIO test")
pause()