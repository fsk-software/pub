import time;

StartTime=time.time();
def currentTime():
  return time.time()-StartTime;

ControlLoopCycle=0.10;
class Shaper:
  def __init__(self,val):
    self.pRef_=val;
    self.pResponse_=self.pRef_;
    self.lastTs_=currentTime();
    self.previousError_=0;
    self.integral_=0;
    self.pV_=0.0;
    self.step();
  
  def moveTo(self,val):
    self.pRef_=val;

  def position(self):
    return self.pResponse_;

  def step(self, dt=None):
    #--ref to: http://www.codeproject.com/Articles/36459/PID-process-control-a-Cruise-Control-example
    Kp=1.0;
    Ki=0.003;
    Kd=1;
    noise=0.0;
    tS=currentTime();
    if dt == None:
      dT=tS-self.lastTs_;
    else:
      dT=dt;
    error=self.pRef_-self.pResponse_;
    self.integral_=self.integral_+error*dT;
    derivative=(error-self.previousError_)/dT;
    output=Kp*error+Ki*self.integral_+Kd*derivative;
    self.previousError_=error;
    self.pV_=self.pV_+(output*0.20)-(self.pV_*0.10)+noise;
    dP=self.pV_*dT;
    self.pResponse_ = self.pResponse_+dP;
#   print "%.2f %.2f"%(self.pRef_,self.pResponse_);
    self.lastTs_=tS;

    if dt==None:
      time.sleep(ControlLoopCycle);
#   print self.__dict__;

