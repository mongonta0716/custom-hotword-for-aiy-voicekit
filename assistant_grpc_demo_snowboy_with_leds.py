#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google Assistant GRPC recognizer."""

import argparse
import locale
import logging
import sys

import aiy.assistant.grpc
import aiy.audio
import aiy.voicehat
from aiy.leds import Leds, Pattern, RgbLeds
from aiy.i18n import set_language_code

import mod.snowboydecoder as snowboydecoder
import sys

RED = (0xFF, 0x00, 0x00)
GREEN = (0x00, 0xFF, 0x00)
YELLOW = (0xFF, 0xFF, 0x00)
BLUE = (0x00, 0x00, 0xFF)
PURPLE = (0xFF, 0x00, 0xFF)
CYAN = (0x00, 0xFF, 0xFF)
WHITE = (0xFF, 0xFF, 0xFF)


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

def volume(string):
    value = int(string)
    if value < 0 or value > 100:
        raise argparse.ArgumentTypeError('Volume must be in [0...100] range.')
    return value

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def main():
    logging.basicConfig(level=logging.DEBUG)
    leds = Leds()

    parser = argparse.ArgumentParser(description='Assistant service example')
    parser.add_argument('--language',
                        default=locale_language(),
                        help='language_code')
    parser.add_argument('--volume', type=volume, default=100)
    parser.add_argument('--model', 
                        default='src/mod/resources/alexa/alexa_02092017.umdl',
                        help='trained model of snowboy')
    parser.add_argument('--sensitivity', default=0.5,
                        help='sensitivity of snowboy')
    args = parser.parse_args()

    set_language_code(args.language)

    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status('starting')
    leds.update(Leds.rgb_on(RED))
    assistant = aiy.assistant.grpc.get_assistant()
    detector = snowboydecoder.HotwordDetector(args.model,
                                              sensitivity=args.sensitivity)
    with aiy.audio.get_recorder():
        try:
            while True:
                status_ui.status('ready')
                print('Speak own hotword and speak')
                leds.update(Leds.rgb_on(GREEN))
                detector.start()
                status_ui.status('listening')
                print('Listening...')
                leds.update(Leds.rgb_on(BLUE))
                text, audio = assistant.recognize()
                if text:
                    if (text == 'goodbye') or \
                       (text == 'さようなら') or \
                       (text == '終了'):
                        status_ui.status('stopping')
                        break
                    elif (text == 'シャットダウンして'):
                        status_ui.status('stopping')

                    print('You said "', text, '"')
                if audio:
                    leds.update(Leds.rgb_on(YELLOW))
                    aiy.audio.play_audio(audio, assistant.get_volume())
        except KeyboardInterrupt:
            status_ui.status('stopping')
        finally:
            print('Bye!')
            leds.reset()


if __name__ == '__main__':
    main()
