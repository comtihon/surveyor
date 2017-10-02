#!/usr/bin/env bash
if [ ! -d  "$HOME/services" ]; then
  cp build_images.sh $HOME/build_images.sh
  cd $HOME
  bash build_images.sh
fi