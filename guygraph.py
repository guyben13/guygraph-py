from math import *
import pygame
from pygame.locals import *
import random

_clock = None
_window = None
_width = 600
_height = 300
_keys = {}
_images = {}
_sprites = {}

AUTO_UPDATE = True

def _autoupdate():
  if AUTO_UPDATE:
    pygame.display.update()

def InitScreen(width, height, auto_update=True):
  global _window, _clock, AUTO_UPDATE, _width, _height
  if _window is not None:
    CloseScreen()

  _keys = {}
  _images = {}
  _sprites = {}
  _width = width
  _height = height
  pygame.init()
  _window = pygame.display.set_mode((width, height))
  _clock = pygame.time.Clock()
  AUTO_UPDATE = auto_update

def CloseScreen():
  global _window
  if _window is None:
    return
  _window = None
  pygame.quit()

def _get_window():
  global _window
  if _window is None:
    InitScreen(_width, _height)
  return _window

def ScreenWidth():
  return _get_window.get_width()

def ScreenHeight():
  return _get_window.get_height()

def UpdateScreen():
  window = _get_window()
  pygame.display.update()

def ClearScreen(c=(0, 0, 0)):
  window = _get_window()
  window.fill(c)
  _autoupdate()

def PutPixel(x, y, c=(255, 255, 255)):
  window = _get_window()
  window.set_at((int(x), int(y)), c)
  _autoupdate()

def GetPixel(x, y):
  window = _get_window()
  return window.get_at((int(x), int(y)))

def DrawLine(x0, y0, x1, y1, c=(255, 255, 255), w=1):
  window = _get_window()
  pygame.draw.line(
      window, c, (x0, y0), (x1, y1),
      width=w)
  _autoupdate()

def DrawRect(x, y, width, height, c=(255, 255, 255), w=0, r=0):
  window = _get_window()
  pygame.draw.rect(
      window, c,
      pygame.Rect((x, y), (width, height)),
      width=w, border_radius=r)
  _autoupdate()

def DrawCircle(x, y, r, c=(255, 255, 255), w=0):
  window = _get_window()
  pygame.draw.circle(window, c,
      (x,y),
      r, width=w)
  _autoupdate()

def _arange_text(font, text):
  if isinstance(text, str):
    text = [text]
  text = sum([i.split('\n') for i in text], [])
  w=0
  h=0
  res=[]
  for t in text:
    dw, dh = font.size(t)
    res.append((0, h, t))
    h += dh
    w = max(w, dw)
  return w, h, res

def DrawText(x, y, text, c=(255,255,255), s=20, font="Monospace"):
  window = _get_window()
  font = pygame.font.SysFont(font, int(s))
  w, h, texts = _arange_text(font, text)
  for dx,dy,t in texts:
    surface = font.render(t, True, c)
    window.blit(surface, (x+dx, y+dy))
  _autoupdate()
  return w, h

def _create_error_sprite(text):
  print(text)
  c=(255,255,255)
  s=10
  font="Monospace"
  line_c=(255, 0, 0)
  window = _get_window()
  font = pygame.font.SysFont(font, int(s))
  w, h, texts = _arange_text(font, text)
  res = pygame.Surface((w+1,h+1), 0, window)
  pygame.draw.rect(
      res, line_c,
      pygame.Rect((0,0), (w,h)),
      width=1)
  pygame.draw.line(
      res, line_c,
      (0,0), (w,h),
      width=1)
  pygame.draw.line(
      res, line_c,
      (0,h), (w,0),
      width=1)
  for dx,dy,t in texts:
    surface = font.render(t, True, c)
    res.blit(surface, (dx, dy))
  return res

def _get_sprite(name):
  res = _sprites.get(name, None)
  if res is None:
    res = _create_error_sprite(f"Error:\nCouldn't find sprite named\n{name}")
    _sprites[name] = res
  return res

def DrawSprite(name, x, y):
  window = _get_window()
  sprite = _get_sprite(name)
  window.blit(sprite, (x,y))
  _autoupdate()

def CopyToSprite(name, x, y, w, h, remove_color=None):
  window = _get_window()
  sprite = window.subsurface(pygame.Rect((x, y), (w, h))).copy()
  if remove_color is not None:
    sprite.set_colorkey(remove_color)
  _sprites[name] = sprite

def LoadSprite(name, fname):
  window = _get_window()
  if fname not in _images:
    try:
      image = pygame.image.load(fname).convert_alpha(window)
    except (pygame.error, FileNotFoundError) as e:
      print(f"Error reading file {fname}: {e}")
      image = _create_error_sprite(f"Error loading sprite {name}\nProblem reading file\n{fname}")
    _images[fname] = image
  else:
    image = _images[fname]
  _sprites[name] = image
  return image.get_size()

def CreateSubsprite(name, x,y,w,h, new_name):
  window = _get_window()
  sprite = _get_sprite(name)
  sub_sprite = sprite.subsurface(pygame.Rect((x, y), (w, h)))
  _sprites[new_name] = sub_sprite
  return sub_sprite.get_size()

def SpriteWidth(name):
  return _get_sprite(name).get_width()

def SpriteHeight(name):
  return _get_sprite(name).get_height()

def Wait():
  window = _get_window()
  if not AUTO_UPDATE:
    UpdateScreen()
  _clock.tick(30)
  return _update_events()

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
  global _window
  if _window is None:
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

def HasScreen():
  return _update_events()

def GetKey(key):
  window = _get_window()
  if not _update_events():
    return 0
  key = _key_mapping[key.upper()]
  res = _keys.get(key, 0)
  if res > 0:
    _keys[key] = res + 1
  return res

