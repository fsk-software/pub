import Logger;
import threading;
import Device;
import time;
import Time;
from pylab import *;


loader_=Device.Device("loader");
shuttle_=Device.Device("shuttle");
flopTray_=Device.Device("flopTray");
rammer_=Device.Device("rammer");
donePlotting=False;
#seqNum=0;

def mainLoop():
  plt.ion();
  fig=plt.figure(1);
  ax1=fig.add_subplot(511);
  ax1.set_ylabel(loader_.name());
  ax2=fig.add_subplot(512);
  ax2.set_ylabel(shuttle_.name());
  ax3=fig.add_subplot(513);
  ax3.set_ylabel(flopTray_.name());
  ax4=fig.add_subplot(514);
  ax4.set_ylabel(rammer_.name());
  ax5=fig.add_subplot(515);
  ax5.set_ylabel("sequencer");

  l1,=ax1.plot(100,100,'r-');
  l2,=ax2.plot(100,100,'r-');
  l3,=ax3.plot(100,100,'r-');
  l4,=ax4.plot(100,100,'r-');
  l5,=ax5.plot(100,100,'r-');

  global donePlotting;
  seqD=[];
  step=0;
  while (not donePlotting):

    D1 = loader_.pList();
    T1=[x[0] for x in D1];
    L1=[x[1] for x in D1];
    l1.set_xdata(T1);
    l1.set_ydata(L1);
    ax1.set_ylim([0,105]);
    ax1.set_xlim([min(T1),max(T1)]);

    D2 = shuttle_.pList();
    T2=[x[0] for x in D2];
    L2=[x[1] for x in D2];
    l2.set_xdata(T2);
    l2.set_ydata(L2);
    ax2.set_ylim([0,95]);
    ax2.set_xlim([min(T2),max(T2)]);

    D3 = flopTray_.pList();
    T3=[x[0] for x in D3];
    L3=[x[1] for x in D3];
    l3.set_xdata(T3);
    l3.set_ydata(L3);
    ax3.set_ylim([0,45]);
    ax3.set_xlim([min(T3),max(T3)]);

    D4 = rammer_.pList();
    T4=[x[0] for x in D4];
    L4=[x[1] for x in D4];
    l4.set_xdata(T4);
    l4.set_ydata(L4);
    ax4.set_ylim([0,180]);
    ax4.set_xlim([min(T4),max(T4)]);

    seqD.append((Time.currentTime(),step));
    T5=[x[0] for x in seqD];
    L5=[x[1] for x in seqD];
    l5.set_xdata(T5);
    l5.set_ydata(L5);
    ax5.set_ylim([0,15]);
    ax5.set_xlim([min(T4),max(T4)]);

    #--update sequencer
    if (step==0):
      #--move everything home
      loader_.moveTo(15);
      shuttle_.moveTo(0);
      flopTray_.moveTo(0);
      rammer_.moveTo(0);
      if (loader_.position() < 16 and shuttle_.position() < 1 and flopTray_.position() < 1 and rammer_.position() < 1):
        step=1;
    elif(step==1):
      #--move propellant to flopTray
      shuttle_.moveTo(90);
      if (shuttle_.position() >= 89):
        step=2;
    elif(step==2):
      #--move flopTray to receive projectile & move shuttle to grab projectile
      flopTray_.moveTo(30);
      shuttle_.moveTo(0);
      if(flopTray_.position() > 29 and shuttle_.position() < 1):
        step=3;
    elif(step==3):
      #--move projectile to flopTray
      shuttle_.moveTo(90);
      if (shuttle_.position() >= 89):
        step=4;
    elif(step==4):
      #--move loader to breech and home shuttle
      loader_.moveTo(90);
      shuttle_.moveTo(0);
      if (loader_.position() >= 89):
        step=5;
    elif(step==5):
      #--ram projectile
      rammer_.moveTo(178);
      if (rammer_.position() >= 177):
        step=6;
    elif(step==6):
      #--retract rammer
      rammer_.moveTo(0);
      if (rammer_.position() <= 1):
        step=7;
    elif(step==7):
      #--shift propellant on flopTray
      flopTray_.moveTo(0);
      if (flopTray_.position() <= 1):
        step=8;
    elif(step==8):
      #--ram propellant
      rammer_.moveTo(178);
      if (rammer_.position() >= 177):
        step=9;
    elif(step==9):
      loader_.moveTo(15);
      if(loader_.position() <= 16):
        step=10;
    elif(step==10):
        print "BANG!!!"
        step=0;

    plt.draw();
    plt.pause(0.1);

def quit():
  global donePlotting;
  donePlotting=True;

def run():
  Logger.log("running sequencer");

  threading.Timer(95.0, quit).start();

  mainLoop();

  loader_.stop();
  shuttle_.stop();
  flopTray_.stop();
  rammer_.stop();

