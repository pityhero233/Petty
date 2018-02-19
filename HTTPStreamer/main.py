import os

res=os.system('''./mjpg-streamer/mjpg-streamer-experimental/mjpg_streamer -i "input_uvc.so -f 10 -y" -o "output_http.so -c "pityhero:pityhero:" -w www -p 8888" -o "output_file.so -d 1000 -f /home/void/projects/Petty/HTTPStreamer/cache/"''')

