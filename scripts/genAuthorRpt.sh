#!/bin/bash
# Author: Noah Gold
gitinspector -lrTw --file-types=py,js,html,sh,css --exclude=env --exclude=migrations --exclude=bower_components --exclude=animate.css --exclude=bootstrap.css --exclude=bootstrap.js --exclude=bootstrap -F html > authorRpt.html --since=$1 --until=$2
