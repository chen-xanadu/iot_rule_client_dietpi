#!/bin/bash

while true
do
  lftp sftp://{user}:@{server} -e "mirror -R --Move {data_dir}/ uploads; bye"
  sleep {interval}
done

