# Sys Stats Restful

I just simply need a restful API that can tell the HA (Home Assistant) service about CPU temperature of the home router, which is running over KVM virtualization on a compact size SBC with only passive cooling. 

So this is it, done in kinda less than 3 hours, not quite sophisticated or flexible though. 

-----

## What can this offer

```commandline
curl http://<hostname>:9090/stats
```

It returns the sensor data immediately. 

```commandline
{
    "du": {
        "free_size": 4177.87,
        "free_rate": 29.4
    },
    "temps": {
        "cpu_thermal": {
            "curr": 59.44,
            "crit": 100.0
        },
        "gpu_thermal": {
            "curr": 58.89,
            "crit": 95.0
        }
    }
}
```

-----

## How To Make This Work

1. Clone the repo, and set up python3 based virtual env. 
2. Install the pip dependencies using the ```requirements.txt``` included.
3. Run the service with ```python entry.py```.
4. Check if the service works well through http clients like ```curl http://<hostname>:9090/stats```.
5. Optional - if it's all good, refer the ```sys_stats_restful.service``` to set up systemd service, then the service can survive after reboot. 
6. Optional - integrate the service with HA by the ```to_be_placed_in_ha_configuration.yaml``` to show the data on HA dash. 
-----

## Configuration of my HW/OS

1. An ARM based SBC (Asus Tinker Board 2s) with Armbian as host OS, kernel version ```6.1.x #1 SMP PREEMPT aarch64 GNU/Linux```.
2. OpenWrt ```Snapshot 23.x``` runs over KVM on the Armbian, which has 2 virtual eth interfaces bridged with 802.1q VLAN interfaces of Armbian. 
3. The CPU and GPU temperature of the SBC can be viewed by ```sensors``` in terminal after ```apt install lm-sensors```. 
4. This service can be deployed either in Armbian (on bare metal hardware) or docker/lxc if you prefer, as long as the code can extract the necessary data from certain paths of host OS. I suppose a deployment in KVM based vm is NOT OK because the data can not be fetched in that level of hardware isolation.
