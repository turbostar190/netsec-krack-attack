#!/bin/bash

# Avvia tre script Python in tre finestre del terminale diverse

xfce4-terminal --title="AP" --command="python3 -i ./ap.py"
xfce4-terminal --title="MitM" --command="python3 -i ./mitm.py"
xfce4-terminal --title="Client" --command="python3 -i ./client.py"
