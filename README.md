# PrisonersDilemma_Strategy
Prisoners Dilemma with Tit-for-Tat and Random strategy with an angry or sad Cozmo


## Requirements
Two Cozmo robots
Two Android tablets with Cozmo version 1.5 installed on it. 

Python 3.5.3 with following packages installed
numpy==1.16.4
Pillow==6.1.0
cozmoclad==1.5.0
cozmo==0.14.0

The cozmo sdk(s) are a match for version Cozmo app version 3.4 . They need to be installed in order provided so that a newer version of the packages don't get pulled in. To install Cozmo app see [here](https://github.com/cozmo4hri/Device_Setup)

To setup your device and computer to run custom python code, see instruction from Anki here: http://cozmosdk.anki.com/docs/initial.html

Note: To use later versions of the Cozmo app you might need to revisit the animations that have been updated.

To run commands, exmamples:

Practice: python tap_game.py --participantID=4 --strategy=P --colour=R --singleScreen

Baseline: python tap_game.py --participantID=2 --strategy=B --colour=R --singleScreen

