#!/bin/bash

# Avvia tre script Python in tre finestre del terminale diverse

gnome-terminal --name="AP" --command="python3 -i ./ap.py"
gnome-terminal --name="MitM" --command="python3 -i ./mitm.py"
gnome-terminal --name="Client" --command="python3 -i ./client.py"
