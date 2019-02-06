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
from aiy.i18n import set_language_code

import mod.snowboydecoder as snowboydecoder
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

def volume(string):
    value = int(string)
    if value < 0 or value > 100:
        raise argparse.ArgumentTypeError('Volume must be in [0...100] range.')
    return value

def sensitivity(string):
    value = float(string)
    if value <= 0 or value > 1:
        raise argparse.ArgumentTypeError('Sensitiviti must be float between 0 and 1.')
    return value

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Assistant service example')
    parser.add_argument('--language',
                        default=locale_language(),
                        help='language_code')
    parser.add_argument('--volume', type=volume, default=100)
    parser.add_argument('--model', 
                        default='src/mod/resources/alexa/alexa_02092017.umdl',
                        help='trained model of snowboy')
    parser.add_argument('--sensitivity',
                        type=sensitivity,
                        default=0.5,
                        help='sensitivity of snowboy')
    args = parser.parse_args()

    set_language_code(args.language)

    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status('starting')
    assistant = aiy.assistant.grpc.get_assistant()
    detector = snowboydecoder.HotwordDetector(args.model,
                                              sensitivity=args.sensitivity)
    with aiy.audio.get_recorder():
        try:
            while True:
                status_ui.status('ready')
                print('Speak own hotword and speak')
                detector.start()
                status_ui.status('listening')
                print('Listening...')
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
                    aiy.audio.play_audio(audio, assistant.get_volume())
        except KeyboardInterrupt:
            status_ui.status('stopping')
        finally:
            print('Bye!')


if __name__ == '__main__':
    main()
