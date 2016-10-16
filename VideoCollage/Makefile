
all:
	${SH} bash -c "sleep 2; xterm -e tail -f ./run.out" &
	${SH} time stdbuf -eL ./run >> ./run.out 2>&1

collage:
	${RM} ./files.txt
	${SH} for f in `ls -r video-???.mp4`; do echo "file '$$f'" >> ./files.txt; done
	${SH} ffmpeg -y -f concat -i ./files.txt -c copy ./video.mp4

clean:
	${RM} *.mp4 *.mkv *.webm *.png files.txt
