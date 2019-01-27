# custom-hotword-for-aiy-voicekit
Snowboy API for AIY Voice Kit.    
Replace your AIY Voice Kit hotword [OK. Google] to [alexa],[jarvis]...etc  
You can easily replace your program.  

# Requirement

- [AIY Kits Release 2018-08-03](https://github.com/google/aiyprojects-raspbian/releases/tag/v20180803)
- Google AIY Voice Kit V2

# Before How to install
Buy The AIY Voice Kit and complete the tutorial.  
custom-hotword-for-aiy-voicekit use lowlevel api AIY Voice Kit.

https://aiyprojects.withgoogle.com/voice/

Are you work your voice kit this program?
```
src/examples/voice/assistant_grpc_demo.py
```
If the demo has worked,next step.

# How to install

```
cd /home/pi/
# libatlas-base-dev need snowboy module.
sudo apt-get install libatlas-base-dev

# copy snowboy module and sample program.
cp -ipr custom-hotword-for-aiy-voicekit/mod ~/AIY-projects-python/src/
cp -ip custom-hotword-for-aiy-voicekit/assistant_grpc_demo_snowboy.py ~/AIY-projects-python/src/examples/voice/
```

# How to use

```
AIY-projects-shell.sh
chmod a+x src/examples/voice/assistant_grpc_demo_snowboy.py
src/examples/voice/assistant_grpc_demo_snowboy.py --model=src/mod/resources/alexa/alexa_02092017.umdl
```
Say "alexa" and talk your google assistant!

sample log
```
pi@raspberrypi:~/AIY-voice-kit-python $ src/examples/voice/assistant_grpc_demo_snowboy.py src/mod/resources/alexa/alexa_02092017.umdl
/opt/aiy/projects-python/src/aiy/_drivers/_led.py:51: RuntimeWarning: This channel is already in use, continuing anyway.  Use GPIO.setwarnings(False) to disable warnings.
  GPIO.setup(channel, GPIO.OUT)
[2018-06-03 14:33:26,194] INFO:recorder:started recording
Speak own hotword and speak
[2018-06-03 14:33:28,634] INFO:snowboy:Keyword 1 detected at time: 2018-06-03 14:33:28
Listening...
[2018-06-03 14:33:31,478] INFO:speech:transcript: What
[2018-06-03 14:33:31,483] INFO:speech:transcript: What is
[2018-06-03 14:33:31,485] INFO:speech:transcript: What is your
[2018-06-03 14:33:31,487] INFO:speech:transcript: What is 4
[2018-06-03 14:33:31,489] INFO:speech:transcript: What is よね
[2018-06-03 14:33:31,491] INFO:speech:transcript: What is your name
[2018-06-03 14:33:31,492] INFO:speech:transcript: What  is your name
[2018-06-03 14:33:31,494] INFO:speech:transcript: What is  your name
[2018-06-03 14:33:31,496] INFO:speech:event_type: 1
[2018-06-03 14:33:31,501] INFO:speech:transcript: What is your name
You said " What is your name "
Speak own hotword and speak
```

# Make your own hotword
Make your own hotword this site.   
and download your voice kit [hotword].pmdl  
(how to make your hotword by snowboy, google it ^^!)

https://snowboy.kitt.ai/

and run program argument your hotword

```
cd AIY-voice-kit-python
src/examples/voice/assistant_grpc_demo_snowboy.py --model=[hotword].pmdl
```

