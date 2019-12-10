#!/bin/bash

git submodule update --remote --rebase www
cd www

if [[ ! -d node_modules ]]; then
  echo "You need to run npm install in www first!"
  exit 0
fi

npm run build

cd ..
echo | gcloud app deploy