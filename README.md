# JPE Cryo Positioning Systems Controller (CAB1-115) for Liger (WMKO)

## Example Usage

```bash
# Move actuator in positive direction until it reaches the maximum actuation steps with frequency of 200Hz at 300 Kelvin
python3 liger_piezo_controller -a 192.168.0.1 -d 1 -f 200 -s 0 -t 300
```

### Argument Options
* ```-a/--addresss``` : IP Address of JPE CAB1-115 Unit (Example: 192.168.0.1)
* ```-d/--direction``` : Direction (1 for positive movement and 0 for negative movement) [Default: 1]
* ````-f/--frequency``` : Frequency (1[Hz] to 600[Hz]) [Default: 300[Hz]]
* ```-s/--step``` : Number of actuation steps. Range 0 to 5000, where 0 is used for infinite move [Default: 0]
* ```-t/--temperature``` : Temperature of the environment in which the actuator is used in Kelvin[K]. Range 0[K] to 300[K]. [Default: 300[K]]
* ```--stop``` : Immediately stop the liner actuator