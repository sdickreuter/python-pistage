__author__ = 'sei'

import PIStage
import time
from datetime import datetime
import math

_number_of_samples = 100
_integration_time = 0.01
_cycle_time = 0  # cycle duration in s
_cycle_time_start = 3 * _integration_time * 1000 / 10  # cycle duration in s, starting value
_cycle_factor = -float(180) / _number_of_samples  # cycle time is calculated using this factor
_amplitude = 5

def _millis():
    dt = datetime.now() - _starttime
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms


#stage = PIStage.E545()

#stage.home()
#stage.moveabs(10,10,10)
time.sleep(0.1)

_starttime = datetime.now()
bla = 0
t0 = 0
for i in range(_number_of_samples):
    t = _millis() / 1000
    dt = t-t0
    t0 = t

    _cycle_time = 0.5 #_cycle_factor * t + _cycle_time_start
    ref = math.cos(2* math.pi * t / _cycle_time )
    #delta = math.sin(2*math.pi*t/_cycle_time)/(dt*1000)

    #stage.moverel(dx=_amplitude*delta)
    time.sleep(_integration_time)
    #pos = stage.pos()
    #print "Pos: {0:+8.4f} | t: {1:6.3f}".format(pos[0],t) + '  ' + '#'.rjust(10*int(round(((pos[0]-10)/_amplitude)+5,0)))
    print "Ref: {0:+8.4f} | t: {1:7.3f}".format(ref,t) + '  ' + '#'.rjust(int(round(2*(bla-10)))+50)
