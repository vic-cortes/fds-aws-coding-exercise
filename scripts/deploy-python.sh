#!/bin/bash

mkdir .temp
mkdir .temp/package

uv pip install -r app/python/requirements.txt --target .temp/package
pip install \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version 3.13 \
  --only-binary=:all: \
  --target .temp/package \
  --upgrade pydantic

cp -r app/python/src/. .temp/package

cd .temp/package
zip -r ../package.zip .
cd ../..

aws lambda update-function-configuration \
    --profile "fender" \
    --function-name fender_digital_code_exercise \
    --runtime python3.13 \
    --handler main.handler

aws lambda update-function-code \
    --profile "fender" \
    --function-name fender_digital_code_exercise \
    --zip-file fileb://.temp/package.zip 

rm -rf .temp