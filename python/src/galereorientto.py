  def orientTo(self, **args):
    targetTheta = args['theta']
    speed = 30 if 'speed' not in args else args['speed']
    threshold = pi/100 if 'threshold' not in args else args['threshold']
    clockwise = None if 'clockwise' not in args else args['clockwise']

    self.done = False
    theta = self.positionWatcher.getTheta()
    self.logger.info("OrientTo", {
      'currentTheta': degrees(theta),
      'targetTheta': degrees(targetTheta),
      'clockwise': bool(clockwise),
      'speed': speed
    })


    while not self.done:
      x, y, theta = self.positionWatcher.getPos()
      if theta > pi: theta -= 2*pi
      if targetTheta > pi: targetTheta -= 2*pi

      clockwiseSpeed = 1 if clockwise else -1
      cmd = speed * clockwiseSpeed

      if abs(cmd * speed) < 15: cmd = 15 * self.sign(cmd)
      if abs(cmd * speed) < 100: cmd = 100 * self.sign(cmd)
      cmdD = cmd
      cmdG = -cmd

      self.platform.setSpeed([cmdG, cmdD])
      
      errorsChoice = [
        (targetTheta - theta),
        (targetTheta + 2*pi - theta),
        (targetTheta - 2*pi - theta)
      ]
      formattedChoices = list(map(lambda p: abs(p), errorsChoice))
      orientationError = errorsChoice[formattedChoices.index(min(formattedChoices))]
      
      #orientationError = t1 if abs(t1) < abs(t2) else t2
      
      print("\n\norientationError",degrees(orientationError))
      print("targetTheta",degrees(targetTheta))
      print("theta",degrees(theta))
      print("speeds",[cmdG, cmdD])
      

      if abs(orientationError) < threshold:
        self.done = True

    self.platform.stop()
    self.logger.info("End of OrientTo", round(degrees(theta), 2))
