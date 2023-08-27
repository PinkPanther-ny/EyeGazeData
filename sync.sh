#!/bin/bash

pgrep -af "ssh.*-p 55555.*-L 6048"
pkill -f "ssh.*-p 55555.*-L 6048"

ssh -N -f -p 55555 -L 6048:10.16.100.48:22 firefly
rsync -av --ignore-existing --progress ./images local48:/home/dujw/alvin/2023/EyeGaze