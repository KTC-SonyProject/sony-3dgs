#!/bin/bash

poetry config virtualenvs.in-project true

# create .env file
# もし.envファイルがなければ作成する
if [ ! -e .env ]; then
  cp .env.sample .env
fi