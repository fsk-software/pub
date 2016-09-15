import threading;
import Logger;
import collections;
import Time;
import time;
import random;

MaxLen=256;
ControlLoopStep=0.5;
ControlLoopCycle=0.10;

class Device(threading.Thread):
  def __init__(self,name):
    Logger.log("Device::__init__() entry");
    self.lock_ = threading.Lock();
    self.name_=name;
    self.done_ = False;
    threading.Thread.__init__(self);
    self.pResponse_ = random.randrange(0,180);
    self.pRef_ = self.pResponse_;
    self.D_=[];
    self.D_ = collections.deque(maxlen=MaxLen);
    self.a_=10;
    self.v_=0.0;
    self.start();
    Logger.log("Device::__init__() exit");

  def name(self):
    return self.name_;

  def stop(self):
    self.lock_.acquire();
    self.done_ = True;
    self.lock_.release();

  def moveTo(self,position):
    self.lock_.acquire();
    self.pRef_ = position;
    self.lock_.release();

  def position(self):
    self.lock_.acquire();
    retVal=self.pResponse_;
    self.lock_.release();
    return retVal;
    
  def run(self):
    #--ref to: http://www.codeproject.com/Articles/36459/PID-process-control-a-Cruise-Control-example

    lastTs=Time.currentTime();
    previousError=0;
    integral=0;
    Kp=1.2;
    Ki=0.003;
    Kd=1;
    pV=0.0;
    noise=0.0;
    while(not self.done_):
      self.lock_.acquire();

      tS=Time.currentTime();
      dT=tS-lastTs;
      error=self.pRef_-self.pResponse_;
      integral=integral+error*dT;
      derivative=(error-previousError)/dT;
      output=Kp*error+Ki*integral+Kd*derivative;
      previousError=error;
      pV=pV+(output*0.20)-(pV*0.10)+noise;
      dP=pV*dT;
      self.pResponse_ = self.pResponse_+dP;
      lastTs=tS;

#     self.pResponse_ = self.pResponse_ + dP;
      self.D_.append((Time.currentTime(),self.pResponse_));

      self.lock_.release();
      time.sleep(ControlLoopCycle);

  def pList(self):
    L=[];
    self.lock_.acquire();
    L.extend(self.D_);
    self.lock_.release();
    return L;


