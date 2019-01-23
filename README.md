# custom-hotword-for-aiy-voicekit
Snowboy API for AIY Voice Kit.    
Replace your AIY Voice Kit hotword [OK. Google] to [alexa],[jarvis]...etc  
You can easily replace your program.  
See. [diff AIY Voice Kit Press button and own hotword program](#diff-original-programaiy-voice-kit-press-button-snowboy-wakeword-program)

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
sudo apt install libatlas-base-dev
git clone https://github.com/mongonta0716/custom-hotword-for-aiy-voicekit

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
INFO:root:Speak own hotword and speak
DEBUG:snowboy:detecting...
INFO:snowboy:detect started.
INFO:snowboy:Keyword 1 detected at time: 2019-01-22 18:56:48
INFO:snowboy:detect stopped.
DEBUG:snowboy:detect voice break
DEBUG:snowboy:finished.
INFO:root:Conversation started!
INFO:aiy.assistant.grpc:Recording started.
INFO:aiy.assistant.grpc:You said: "what".
INFO:aiy.assistant.grpc:You said: "what time".
INFO:aiy.assistant.grpc:You said: "what  time".
INFO:aiy.assistant.grpc:You said: "what  time is".
INFO:aiy.assistant.grpc:You said: "what  time is it".
INFO:aiy.assistant.grpc:You said: "what time  is it".
INFO:aiy.assistant.grpc:You said: "what time  is it now".
INFO:aiy.assistant.grpc:You said: "what time is  it now".
INFO:aiy.assistant.grpc:You said: "what time is it  now".
INFO:aiy.assistant.grpc:You said: "what time is it  now".
INFO:aiy.assistant.grpc:You said: "what time is it now".
INFO:aiy.assistant.grpc:End of audio request detected.
INFO:aiy.assistant.grpc:You said: "what time is it now".
INFO:aiy.assistant.grpc:Recording stopped.
DEBUG:aiy.assistant.grpc:Updating conversation state.
INFO:aiy.assistant.grpc:Assistant said: "The time is 6:56."
INFO:aiy.assistant.grpc:Not expecting follow-on query from user.
INFO:aiy.assistant.grpc:Playing started.
INFO:aiy.assistant.grpc:Playing stopped.
INFO:root:Speak own hotword and speak
DEBUG:snowboy:detecting...
INFO:snowboy:detect started.
```

# Make your own hotword
Make your own hotword this site.   
and download your voice kit [hotword].pmdl  
(how to make your hotword by snowboy, google it ^^!)

https://snowboy.kitt.ai/

and run program argument your hotword

```
AIY-projects-shell.sh
src/examples/voice/assistant_grpc_demo_snowboy.py --model=[hotword].pmdl
```

# diff original program(AIY Voice Kit Press button), snowboy wakeword program
```
$ diff -u src/examples/voice/assistant_grpc_demo.py src/examples/voice/assistant_grpc_demo_snowboy.py
--- src/examples/voice/assistant_grpc_demo.py   2018-11-16 17:42:45.417861708 +0900
+++ src/examples/voice/assistant_grpc_demo_snowboy.py   2019-01-23 17:34:31.759182512 +0900
@@ -24,6 +24,8 @@
 from aiy.assistant.grpc import AssistantServiceClientWithLed
 from aiy.board import Board

+import mod.snowboydecoder as snowboydecoder
+
 def volume(string):
     value = int(string)
     if value < 0 or value > 100:
@@ -41,15 +43,17 @@
     parser = argparse.ArgumentParser(description='Assistant service example.')
     parser.add_argument('--language', default=locale_language())
     parser.add_argument('--volume', type=volume, default=100)
+    parser.add_argument('--model', default='src/mod/resources/alexa/alexa_02092017.umdl')
     args = parser.parse_args()

+    detector = snowboydecoder.HotwordDetector(args.model, sensitivity=0.5)
     with Board() as board:
         assistant = AssistantServiceClientWithLed(board=board,
                                                   volume_percentage=args.volume,
                                                   language_code=args.language)
         while True:
-            logging.info('Press button to start conversation...')
-            board.button.wait_for_press()
+            logging.info('Speak own hotword and speak')
+            detector.start()
             logging.info('Conversation started!')
             assistant.conversation()
```
