### 0. darknet-master.zip
- 是没有做修改原始文件，可以后做修改后的文件做对比，方便查看差异

### 1. opencv文件夹

- 存放读取处理视频文件 python脚本：opencvTest.py 
### 2. darknet-master文件夹
- 存放YOLO网络
- 编译网络 
  - cd 到darknet-master，执行make命令，生成 darknet
- 运行darknet 
  - 运行命令  
./darknet detect ./cfg/yolov3-tiny.cfg ../yolov3-tiny.weights /mnt/wsyRamdisk/camera_data.jpg 

  - 在darknet的源码上加了简单的TCP server,这样就可以等待client准备好图片后开始识别

### 3. 数据处理流程
- 新建一个/mnt/wsyRamdisk内存文件夹，提高读取速度
- 开启YOLO网络server
- 运行opencvTest.py 
  截取一张视频图片文件放到 /mnt/wsyRamdisk/camera_data.jpg路径下  
  
- YOLO server在/mnt/wsyRamdisk/camera_data.jpg读取图片并识别  
- YOLO server识别完成后会生成 /mnt/wsyRamdisk/detect_data.txt
- opencvTest.py client 拿到detect_data.txt后在视频中绘制矩形
