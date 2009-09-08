from waveapi import events
from waveapi import model
from waveapi import robot
from waveapi.document import Range
from google.appengine.api import urlfetch
import logging, re

def OnRobotAdded(properties, context):
  """Invoked when the robot has been added."""
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("RequestCluePacker ready")

def OnDocumentChanged(properties, context):
  blips = context.GetBlips()
  for blip in blips:
    text = blip.GetDocument().GetText()
    trkorr_match = re.search(' (SAPK\w{6}|[A-Z0-9]{3}K\d{6}) ', text)
    if trkorr_match:
      trkorr = trkorr_match.group(1)
      logging.info("RE match! '%s'" % (trkorr, ))
      url = "http://sap.pipetree.com:8990/qmacro/request/%s/description" % trkorr
      desc = urlfetch.fetch(url=url).content
      logging.info("Description retrieved: '%s'" % desc)
      if desc:
        text = re.sub(trkorr, "%s-%s" % (trkorr, desc), text)
        blip.GetDocument().InsertText(trkorr_match.end(1), ":'%s' " % desc)

if __name__ == '__main__':
  myRobot = robot.Robot('qmacro-wavebot',
    image_url='http://qmacro-wavebot.appspot.com/assets/icon.png',
    version='B05',
    profile_url='http://qmacro-wavebot.appspot.com/')
  myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
  myRobot.RegisterHandler(events.DOCUMENT_CHANGED, OnDocumentChanged)
  myRobot.Run()

