#!/bin/bash



sleep 30

while true
do
        curr_date=$(date "+%Y_%m_%d_%T")
        pcap_file={tcpdump_dir}/tcpdumpout.$curr_date.pcap
        #sudo timeout 15m tcpdump -i eth0 -s96 -w $pcap_file 2>&1
        sudo timeout 15m tcpdump -i eth0 -n not arp and not ether host `ifconfig eth0 | grep ether | awk '{print $2}' -s96 -w $pcap_file 2>&1


        csv_file={tshart_dir}/tsharkout.$curr_date.csv
        tshark -r $pcap_file -T fields -e frame.number -e frame.time_relative -e _ws.col.Protocol -e frame.len -e frame.time_delta -e eth.src -e eth.dst -e ip.src -e ip.dst -e ip.src_host -e ip.dst_host -e ip.proto -e udp.srcport -e udp.dstport -e ip.len -e udp.length -e tcp.srcport -e tcp.dstport -e tcp.len  -E header=y -E separator=, > $csv_file && rm $pcap_file && mv $csv_file {upload_dir} &
done
