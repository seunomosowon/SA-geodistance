# SA-geodistance

This support add-on adds a reporting command to compute the relative vincenty distances of
adjacent events given their latitudes and longitudes.

It computes the distances in miles by default, but this can be made to give results in kilometres.
This can be done by passing `miles=F` as an argument to the command.

It can also compute the adjacent distances for different groups by passing the grouping criteria, `group_by=group`.

This is only supported after a table command, stats command or other reporting commands.
It currently fails if run against raw events.


## Notes

* Events that do not have latitudes or longitudes, as is the output when geocoding private non-routed IP addresses,
     will be given a distance of 0.0. The next relative distance will still be based on last public address found.

* The first event in the result will also have a distance of 0.0

* This app includes the free unlicensed vincenty library for calculating the distance between two co-ordinates.
Available at: [Vincenty 0.1.4](https://pypi.python.org/pypi/vincenty/0.1.4)


##Syntax


```
<base_search> | geodistance latfield=<field> longfield=<field> output_field=<field> miles=<bool> group_by=<group>
```


##Example 1

This can be used to easily obtain the distance between multiple VPN authentication attempts
which could indicate a compromise where relative distances are above a maximum/expected commutable distance.

```
index=vpn | stats count by src_ip , user | iplocation src_ip | fields src_ip, user, lat, lon  |
    geodistance latfield=lat longfield=lon output_field=distance group_by=user" |
```

##Example 2

This example has been written around the sample app that comes with Splunk.
If the sample app is enabled, some event logs are generated in the sample index.

This search It extracts the clientip field from the relay field,
and geocodes using the inbuilt iplocation search command.

The relative distance in (Km) of each adjacent event is then computed using the `geodistance` command.

```
            "index=sample | rex field=relay \"\[(?<clientip>.*)\]\" |
             iplocation clientip | table lat lon clientip |
             geodistance latfield=lat longfield=lon output_field=distance miles=F"
```


### Support
Support will be provided via Splunkbase :)

All support questions should include the version of Splunk and OS.

Please send feedback and feature requests on splunkbase.
