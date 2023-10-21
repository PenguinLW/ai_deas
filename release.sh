#!/usr/bin/env bash
#in venv
#source ~/venv/bin/activate
#pip install -r req.txt
#pip freeze > req.txt
chmod u+x *.sh *.py
l_dir=pwd

git config --global --add safe.directory $l_dir
#git clone -o ai_deas https://github.com/PenguinLW/ai_deas.git
#git config --global user.email "diana1997525@gmail.com"
#git config --global user.name "PenguinLW"
#git config --global credential.helper cache
git config --global credential.helper "cache --timeout=25200"
#git config credential.helper store
#git config --unset credential.helper

git pull --all
git add .
git commit -m PenguinL
git push --set-upstream ai_deas master
#deactivate
