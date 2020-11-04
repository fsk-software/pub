all: run

run: video.mp4
	${SH} ./vidTracker $<

video.mp4:
	${SH} youtube-dl -f mp4 -o $@ https://www.youtube.com/watch?v=Zyox_fNFXIk 

input.mp4: video.mp4
	${SH} ffmpeg -i $< -pix_fmt argb -vf "geq= r='if(gte(Y,240),0,r(X,Y))': g='if(gte(Y,240),0,g(X,Y))': b='if(gte(Y,240),0,b(X,Y))'" -pix_fmt yuv420p -strict -2 $@

clean:
	${RM} *.mp4 *.pyc
