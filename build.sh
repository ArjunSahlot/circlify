#!/bin/bash

download_link=https://github.com/ArjunSahlot/circlify/archive/main.zip
temporary_dir=$(mktemp -d) \
&& curl -LO $download_link \
&& unzip -d $temporary_dir main.zip \
&& rm -rf main.zip \
&& mv $temporary_dir/circlify-main $1/circlify \
&& rm -rf $temporary_dir
echo -e "[0;32mSuccessfully downloaded to $1/circlify[0m"
