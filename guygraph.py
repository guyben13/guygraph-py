from math import *
import pygame
from pygame.locals import *
import random

pygame.init()
clock = None
window = None

def _point(x, y):
  return int(x), int(y)

def Update():
  global window
  if window is None:
    print("Must call InitScreen")
    return
  pygame.display.update()

AUTO_UPDATE = True

def _autoupdate():
  if AUTO_UPDATE:
    pygame.display.update()

def InitScreen(width, height, auto_update=True):
  global window, clock, AUTO_UPDATE
  if window is not None:
    CloseScreen()
# print("Error! Can only call InitScreen once")
# return
  window = pygame.display.set_mode((width, height))
  clock = pygame.time.Clock()
  AUTO_UPDATE = auto_update

def CloseScreen():
  global window
  if window is None:
    print("Must call InitScreen")
    return
  window = None
  pygame.quit()

def ClearScreen(c=(0, 0, 0)):
  global window
  if window is None:
    print("Must call InitScreen")
    return
  window.fill(c)
  _autoupdate()

def PutPixel(x, y, c=(255, 255, 255)):
  global window
  if window is None:
    print("Must call InitScreen")
    return
  window.set_at(_point(x, y), c)
  _autoupdate()

def GetPixel(x, y):
  global window
  if window is None:
    print("Must call InitScreen")
    return (0, 0, 0, 0)
  return window.get_at(_point(x, y))

def DrawLine(x0, y0, x1, y1, c=(255, 255, 255), w=1):
  global window
  if window is None:
    print("Must call InitScreen")
    return
  pygame.draw.line(
      window, c, (x0, y0), (x1, y1),
      width=w)
  _autoupdate()

def DrawRect(x, y, width, height, c=(255, 255, 255), w=0, r=0):
  global window
  if window is None:
    print("Must call InitScreen")
    return
  pygame.draw.rect(
      window, c,
      pygame.Rect((x, y), (width, height)),
      width=w, border_radius=r)
  _autoupdate()

def DrawCircle(x, y, r, c=(255, 255, 255), w=0):
  global window
  if window is None:
    print("Must call InitScreen")
    return
  pygame.draw.circle(window, c,
      (x,y),
      r, width=w)
  _autoupdate()

def DrawText(x, y, text, c=(255,255,255), s=20, font="Monospace"):
  global window
  if window is None:
    print("Must call InitScreen")
    return
  font = pygame.font.SysFont(font, int(s))
  surface = font.render(text, True, c)
  window.blit(surface, (x, y))
  _autoupdate()

def Wait():
  global window
  if window is None:
    print("Must call InitScreen")
    return
  if not AUTO_UPDATE:
    Update()
  clock.tick(30)

_keys = {}

_key_mapping = {
  "SPACE": pygame.K_SPACE,
  " ": pygame.K_SPACE,
  "ESC": pygame.K_ESCAPE,
  "LSHIFT": pygame.K_LSHIFT,
  "LCTRL": pygame.K_LCTRL,
  "LALT": pygame.K_LALT,
  "RSHIFT": pygame.K_RSHIFT,
  "RCTRL": pygame.K_RCTRL,
  "RALT": pygame.K_RALT,
  "UP": pygame.K_UP,
  "DOWN": pygame.K_DOWN,
  "LEFT": pygame.K_LEFT,
  "RIGHT": pygame.K_RIGHT,
  "A": pygame.K_a,
  "B": pygame.K_b,
  "C": pygame.K_c,
  "D": pygame.K_d,
  "E": pygame.K_e,
  "F": pygame.K_f,
  "G": pygame.K_g,
  "H": pygame.K_h,
  "I": pygame.K_i,
  "J": pygame.K_j,
  "K": pygame.K_k,
  "L": pygame.K_l,
  "M": pygame.K_m,
  "N": pygame.K_n,
  "O": pygame.K_o,
  "P": pygame.K_p,
  "Q": pygame.K_q,
  "R": pygame.K_r,
  "S": pygame.K_s,
  "T": pygame.K_t,
  "U": pygame.K_u,
  "V": pygame.K_v,
  "W": pygame.K_w,
  "X": pygame.K_x,
  "Y": pygame.K_y,
  "Z": pygame.K_z,
  "0": pygame.K_0,
  "1": pygame.K_1,
  "2": pygame.K_2,
  "3": pygame.K_3,
  "4": pygame.K_4,
  "5": pygame.K_5,
  "6": pygame.K_6,
  "7": pygame.K_7,
  "8": pygame.K_8,
  "9": pygame.K_9,
}

def _update_events():
  global window
  if window is None:
    return False
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      _keys[event.key] = 1
    if event.type == pygame.KEYUP:
      _keys[event.key] = 0
    if event.type == pygame.QUIT:
      CloseScreen()
      return False
  return True

def IsRunning():
  return _update_events()

def GetKey(key):
  if not _update_events():
    return 0
  key = _key_mapping[key.upper()]
  res = _keys.get(key, 0)
  if res > 0:
    _keys[key] = res + 1
  return res


