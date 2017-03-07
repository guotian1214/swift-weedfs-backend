# swift-weedfs-backend
seaweedfs backend for openstack-swift

1. bases on mem_diskfile
2. make a little change about seaweedfs CLI [pyseaweed](https://github.com/utek/pyseaweed)

## usage
start seaweedfs
```
weed master -mdir=/home/ubuntu/weedfs
weed volume -dir="/home/ubuntu/weedfs/data1" -mserver="localhost:9333"  -port=8080
weed filer -port=8888
```
change configure file to use in memory object server
```
# in /etc/swift/object-server/
ls | xargs sed -i "s/swift#object/swift#mem_object/"
```
seaweedfs filter server can be set in seaweedfs_operation.py
