all: setup configYolo run

run: sample
	${SH} ./$<

video.mp4:
	${SH} youtube-dl https://www.youtube.com/watch?v=UiBBfWyApyA --format=mp4 -o temp.mp4
	${SH} ffmpeg -y -i temp.mp4 -acodec copy -ss 8 -t 30 $@
	${RM} temp.mp4

video-sm.mp4: video.mp4
	${SH} ffmpeg -i $< -vf scale=iw/4:-1 -acodec copy $@

setup:
	${SH} sudo apt-get install -y libopencv-dev
	${SH} sudo apt-get install -y python3
	${SH} sudo apt-get install -y python3-dev
	${SH} sudo apt-get install -y python3-pip
	${SH} sudo pip3 install pip --upgrade
	${SH} sudo pip3 install opencv-python
	${SH} sudo pip3 install numpy
	${SH} sudo pip3 install cylon
	${SH} sudo pip3 install yolo34py

configYolo: yolov3.cfg yolov3.weights coco.data coco.names sample

yolov3.cfg:
	${SH} wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg

yolov3.weights:
	${SH} wget https://pjreddie.com/media/files/yolov3.weights

coco.data:
	${SH} wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/coco.data
	${SH} mkdir -p data/
	${SH} mv $@ data/

coco.names:
	${SH} wget https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names
	${SH} mkdir -p data/
	${SH} mv $@ data/

darknet:
	${SH} sudo apt-get install -y git
	${SH} git clone https://github.com/pjreddie/darknet.git

sample.jpg: darknet
	${SH} cp $</data/dog.jpg $@

sample: clip01.mp4 sample.jpg
	${SH} touch $@; chmod +x $@
	${SH} echo "#!/usr/bin/python3" >> $@
	${SH} echo "" >> $@
	${SH} echo "from pydarknet import Detector, Image" >> $@
	${SH} echo "import cv2" >> $@
	${SH} echo "" >> $@
	${SH} echo "def test00():" >> $@
	${SH} echo "  net = Detector(bytes('yolov3.cfg', encoding='utf-8'), bytes('./yolov3.weights', encoding='utf-8'), 0, bytes('./data/coco.data',encoding='utf-8'))" >> $@
	${SH} echo "" >> $@
	${SH} echo "  img = cv2.imread('./sample.jpg')" >> $@
	${SH} echo "  img_darknet = Image(img)" >> $@
	${SH} echo "" >> $@
	${SH} echo "  results = net.detect(img_darknet)" >> $@
	${SH} echo "" >> $@
	${SH} echo "  for cat, score, bounds in results:" >> $@
	${SH} echo "      x, y, w, h = bounds" >> $@
	${SH} echo "      cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), thickness=2)" >> $@
	${SH} echo "      cv2.putText(img,str(cat.decode('utf-8')),(int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))" >> $@
	${SH} echo "" >> $@
	${SH} echo "  cv2.imshow('output', img)" >> $@
	${SH} echo "  cv2.waitKey(0)" >> $@
	${SH} echo "" >> $@
	${SH} echo "def test01():" >> $@
	${SH} echo "  net = Detector(bytes('yolov3.cfg', encoding='utf-8'), bytes('./yolov3.weights', encoding='utf-8'), 0, bytes('./data/coco.data',encoding='utf-8'))" >> $@
	${SH} echo "  vidCapture = cv2.VideoCapture('video-sm.mp4')" >> $@
	${SH} echo "  K=0;" >> $@
	${SH} echo "  gotFrame=True;" >> $@
	${SH} echo "  while(vidCapture.isOpened() and gotFrame):" >> $@
	${SH} echo "    gotFrame, frame = vidCapture.read()" >> $@
	${SH} echo "    if gotFrame:" >> $@
	${SH} echo "      print('frame',K);" >> $@
	${SH} echo "      img_darknet = Image(frame);" >> $@
	${SH} echo "      results = net.detect(img_darknet);" >> $@
	${SH} echo "      for cat, score, bounds in results:" >> $@
	${SH} echo "        x, y, w, h = bounds" >> $@
	${SH} echo "        cv2.rectangle(frame, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), thickness=2)" >> $@
	${SH} echo "        cv2.putText(frame,str(cat.decode('utf-8')),(int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))" >> $@
	${SH} echo "#     cv2.imshow('Frame',frame)" >> $@
	${SH} echo "#     if cv2.waitKey(1) & 0xFF == ord('q'):" >> $@
	${SH} echo "#       break " >> $@
	${SH} echo "      cv2.imwrite('frame%05d.jpg'%(K), frame);" >> $@
	${SH} echo "    K+=1;" >> $@
	${SH} echo "  vidCapture.release();" >> $@
	${SH} echo "  cv2.destroyAllWindows();" >> $@
	${SH} echo "#---main---" >> $@
	${SH} echo "#test00()" >> $@
	${SH} echo "test01()" >> $@

clean:
	${RM} -rf darknet data sample sample.jpg yolov3.* frame*jpg video*mp4
