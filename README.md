# SA-geodistance

This support add-on adds a reporting command to compute the relative vincenty/haversine distances of
adjacent events given their latitudes and longitudes.

It uses vincenty method to compute the distances in miles by default, but this can be made to give results in kilometres.
This can be done by passing `miles=F` as an argument to the command.

To use haversine instead, add the paramter `haversine=True` or `haversine=T` 

It can also compute the adjacent distances for different groups by passing the grouping criteria, `group_by=group`.

This currently supports grouping by a single field. A future update will support grouping by multiple fields. 

Available at:
[Splunkbase](https://splunkbase.splunk.com/app/3232/#/details)

[Github](https://github.com/seunomosowon/SA-geodistance)


## Notes

* Events that do not have latitudes or longitudes, as is the output when geocoding private non-routed IP addresses,
     will be given a distance of 0.0. The next relative distance will still be based on last public address found.

* The first event in the result will also have a distance of 0.0

* This app includes the free unlicensed vincenty library for calculating the distance between two co-ordinates.
Available at: [Vincenty 0.1.4](https://pypi.python.org/pypi/vincenty/0.1.4) and 
MIT licensed [haversine 0.4.5](https://pypi.python.org/pypi/haversine).


##Syntax

<code>
<base_search> | geodistance latfield=<field> longfield=<field> output_field=<field> 
                miles=<bool> group_by=<group> haversine=<bool>
</code>


##Example 1

This can be used to easily obtain the distance between multiple VPN authentication attempts
which could indicate a compromise where relative distances are above a maximum/expected commutable distance.

```
index=vpn | stats count by src_ip , user |
iplocation src_ip |
fields src_ip, user, lat, lon  |
geodistance latfield=lat longfield=lon output_field=distance group_by=user
```

##Example 2

This example has been written around the sample app that comes with Splunk.
If the sample app is enabled, some event logs are generated in the sample index.

This search It extracts the clientip field from the relay field,
and geocodes using the inbuilt iplocation search command.

The relative distance in (Km) of each adjacent event is then computed using the `geodistance` command.

S1:
```
	index=sample | rex field=relay \"\[(?<clientip>.*)\]\" |
	iplocation clientip | table lat lon clientip |
	geodistance latfield=lat longfield=lon output_field=distance miles=F
```

S2:
```
	index=sample | rex field=relay "\[(?<clientip>.*)\]" |
		iplocation clientip | table clientip lat lon| search lat=* |
		geodistance latfield=lat longfield=lon output_field=distance group_by=clientip
```

**PS**: the relative distance between all events with the same clientip will be zero


S3:
```
	index=sample | rex field=relay "\[(?<clientip>.*)\]" |
		iplocation clientip | table clientip lat lon from | search lat=* |
	 	geodistance latfield=lat longfield=lon output_field=distance group_by=from | dedup from distance
```


#Enable debug logging

To enable debugging for the geodistance command, add the following to SA-geodistance/local/logging.conf

```
[logger_GeoDistanceCommand]
level = DEBUG
```

Logs are written to $SPLUNK_HOME/var/log/splunk/SA-geodistance.log


### Copyright - Haversine

The Haversine 0.4.5 module is included from [Pypi](https://pypi.python.org/pypi/haversine) 
and is licensed under MIT which permits its use and distribution given the notice below. 

Copyright (c) 2015 Mapado

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

### License

This software is licensed under the [Splunk End User License Agreement for Third-Party Content](https://d38o4gzaohghws.cloudfront.net/static/misc/eula.html)
license agreement.

### Support
Support will be provided via Splunkbase :)

All support questions should include the version of Splunk and OS.

Please send feedback and feature requests on splunkbase.
