# custom-hotword-for-aiy-voicekit
Snowboy API for AIY Voice Kit.    
Google AIY VoiceKit のhotwordを[OK. Google] to [alexa],[jarvis]...といった別のものへ変更できます。
プログラムの変更点はこちらを見てください。 [diff AIY Voice Kit Press button and own hotword program](#diff-original-programaiy-voice-kit-press-button-snowboy-wakeword-program)

# インストールの前に
AIY Voice Kitを購入して、チュートリアルを完了してください。

https://aiyprojects.withgoogle.com/voice/

下記のプログラムが動いたら次のステップへ進みます。
```
src/examples/voice/assistant_grpc_demo.py
```

# インストール方法
## 依存するパッケージをインストールし、custom-hotword-for-aiy-voicekitをgit cloneしてください。
```
cd /home/pi/
sudo apt install libatlas-base-dev
git clone https://github.com/mongonta0716/custom-hotword-for-aiy-voicekit
```

## AIY-project-pythonフォルダに必要なファイルをコピーします。
```
cp -ipr custom-hotword-for-aiy-voicekit/mod ~/AIY-projects-python/src/
cp -ip custom-hotword-for-aiy-voicekit/assistant_grpc_demo_snowboy.py ~/AIY-projects-python/src/examples/voice/
```

# 使い方

下記のようにコマンドを実行してください。

```
AIY-projects-shell.sh
chmod a+x src/examples/voice/assistant_grpc_demo_snowboy.py
src/examples/voice/assistant_grpc_demo_snowboy.py --model=src/mod/resources/alexa/alexa_02092017.umdl
```
「Speak own hotword and speak」と表示されたら
「アレクサ」と言ってGoogleアシスタントに話しかけます。

サンプルログ
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

# 好きなhotwordを使う。
下記のサイトでhotwordを作成します。

https://snowboy.kitt.ai/

詳しい手順は下記のリンクを参照してください。
https://raspberrypi.mongonta.com/snowboy_howtomake_hotword/

作成できたらVoiceKitに[hotword].pmdlというファイルをダウンロードします。
ダウンロード後下記のようにpmdlファイルを指定して実行すると作成したHotwordでVoiceKitが利用できるようになります。
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
