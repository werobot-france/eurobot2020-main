class API:
  def __init__(self, container):
    self.navigation = container.get('navigation')
    self.positionWatcher = container.get('positionWatcher')
    self.elevator = container.get('elevator')
    self.rightClaw = container.get('rightClaw')
    self.leftClaw = container.get('leftClaw')
    self.flag = container.get('flag')
    self.detectionProcess = container.get('detectionProcess')
    self.platform = container.get('platform')
    self.scripts = container.get('scripts')
    self.schlager = container.get('schlager')
    self.platform = container.get('platform')