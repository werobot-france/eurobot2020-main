from math import *

class ToTest:
  Walls = [
    3000, #position y du mur 0
    2000, #position x du mur 1
    0, # position y du mur 2
    0  # position x du mur 3
  ]

  # retourne le mur détécté selon les trucs dessus
  def detectedWall(self, x, y, angle):  
    # rapporter entre -pi et pi
    if angle > pi:
      angle -= 2*pi
    tr = atan2(self.Walls[0] - y, self.Walls[1] - x)
    tl = atan2(self.Walls[0] - y, -x)
    bl = atan2(-y, -x)
    br = atan2(-y, self.Walls[1] - x)
    if angle <= tl and angle >= tr:
      return 0
  
    if angle <= tr and angle >= br:
      return 1
  
    if angle >= bl and angle <= br:
      return 2
  
    if angle >= tl or angle <= bl:
      return 3

    return -1

test = ToTest()
f = test.detectedWall

cases = [
  [[1000, 1500, 0],      1],
  [[1000, 1500, pi/2],   0],
  [[1000, 1500, pi],     3],
  [[1000, 1500, 3*pi/2], 2],
  [[1000, 1500, radians(280)], 2],
  
  [[100, 2700, radians(135)], 3],
  [[500, 2900, radians(340)], 1],
  
  [[500, 2500, radians(135)], 0]
]

for case in cases:
  r = f(case[0][0], case[0][1], case[0][2])
  print(
    ' OK' if r == case[1] else 'ERR', case[0][0], case[0][1], str(round(degrees(case[0][2]), 2)).zfill(6), case[1], r)