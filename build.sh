#!/bin/sh
pyuic4 ./window.ui -o ./windowUi.py
pyrcc4 ./resources.qrc  -o ./resources_rc.py
pyuic4 ./tex_popup.ui -o ./tex_popupUi.py
