---
### OVERVIEW

- About SA-geodistance
- Release notes
- Support and resources

### INSTALLATION

- Hardware and software requirements
- Installation steps 

### USER GUIDE

- Key concepts
- Data types
- Configure SA-geodistance
- Troubleshooting
- Upgrade
- Copyright & License

---
### OVERVIEW

#### About SA-geodistance

| Author | Oluwaseun Remi-Omosowon |
| --- | --- |
| App Version | 1.0 |
| Vendor Products | <ul><li>vincenty-0.1.4 - public domain license </li><li>haversine-0.4.5 - MIT License</li><li>SDK for Python 1.6.0</li></ul> |
| Support-addon | This add-on only needs to be installed on the search heads only (Either standalone or dedicated/clustered)|

The SA-geodistance allows a Splunk® Enterprise user to compute the relative vincenty/haversine distances of
adjacent events given their latitudes and longitudes.

##### Scripts and binaries

Includes:
- Splunk SDK for Python (1.6.0)
- vincenty 0.1.4 - supports the calculation of vincenty distances which is used by default
- haversine 0.4.5 - Supports the use of haversine
- geodistance.py : This is the splunk reporting command introduced by this app


#### Release notes

##### About this release

Version 1.0 of the SA-geodistance is compatible with:

| Splunk Enterprise versions | 6.x |
| --- | --- |
| CIM | Not Applicable |
| Platforms | Platform independent |
| Lookup file changes | No lookups included in this app |

##### New features

SA-geodistance includes the following new features:

- Diagnostic Logging

##### Fixed issues

Version 1.0 of the SA-geodistance doesnt introduce any fixes:


##### Known issues

There are no known issues in version 1.0 of the SA-geodistance


##### Third-party software attributions

Version 1.0 of the SA-geodistance incorporates the following third-party software or libraries.
Available at:  and
MIT licensed .

- [Vincenty 0.1.4](https://pypi.python.org/pypi/vincenty/0.1.4), (public domain)
- [haversine 0.4.5](https://pypi.python.org/pypi/haversine), (https://github.com/mapado/haversine/blob/master/LICENSE)
- [Splunk SDK, 1.6.0] (http://dev.splunk.com/python), (https://www.apache.org/licenses/LICENSE-2.0)


##### Support and resources

**Questions and answers**

Access questions and answers specific to the SA-geodistance at (https://answers.splunk.com/).

**Support**

This Splunk support add-on is community / developer supported.

Questions asked on Splunk answers will be answered either by the community of users or by the developer when available.
All support questions should include the version of Splunk and OS.

You can also contact the developer directly via [Splunkbase] (https://splunkbase.splunk.com/app/3232/).
Feedback and feature requests can also be sent via splunkbase.

Issues can also be submitted at the [SA-geodistance repo via on Github] (https://github.com/seunomosowon/SA-geodistance/issues)

##### Older Releases

* v0.3.8
    - Added logging support
    - Added support for debug logging and documentation for this on README.md
    - Changed to v2 command style

* v0.3.7
    - Updated field descripition for longitude and haversine

* v0.3.5 / 0.3.6
    - Added icons
    - called icons to size

* v0.3.4
    - Updated permission of files
    - Added syntax to search UI

* v0.3.3
    - Fixed logging.conf

* v0.3.1
    - Updated check_for_updates in app.conf

* v0.3
    - Added support for haversine


## INSTALLATION AND CONFIGURATION

### Hardware and software requirements

#### Hardware requirements

SA-geodistance supports the following server platforms in the versions supported by Splunk Enterprise:

- Linux
- Windows

The app was developed to be platform agnostic, but tests are mostly run on unix.
Please contact the developer with issues running this on Windows.

#### Software requirements

To function properly, SA-geodistance has no external requirements but needs to be installed on a full Splunk install
which provides python and the basic math libraries needed.


#### Splunk Enterprise system requirements

Because this add-on runs on Splunk Enterprise, all of the [Splunk Enterprise system requirements](http://docs.splunk.com/Documentation/Splunk/latest/Installation/Systemrequirements) apply.

#### Download

Download the SA-geodistance at [Splunkbase](https://splunkbase.splunk.com/app/3232/) OR [GitHub](https://github.com/seunomosowon/SA-geodistance).

#### Installation steps

To install and configure this app on your supported standalone platform, do one of the following:

- Install on a standalone search head via the GUI (https://docs.splunk.com/Documentation/AddOns/released/Overview/Singleserverinstall)
- Extract the app to ```$SPLUNK_HOME/etc/apps/``` and restart Splunk

For a supported distributed environment, follow the steps to install the SA-geodistance on the search head only.

For a clustered search head environment, install SA-geodistance via the search head deployer.

More instructions available at the following [URL] (https://docs.splunk.com/Documentation/AddOns/released/Overview/Distributedinstall)

For Splunk cloud installations, follow the instructions present at the following [link] (https://docs.splunk.com/Documentation/AddOns/released/Overview/SplunkCloudinstall)


## USER GUIDE

### Key concepts for SA-geodistance

<code>
<base_search> | geodistance latfield=<field> longfield=<field> output_field=<field>
                miles=<bool> group_by=<group> haversine=<bool>
</code>

This app can return distances as miles (default) or kilometer.  To return distances in kilometer,
pass the `miles=F` as an argument to the command.

It computes the vincenty distances by default. To use haversine instead, add the paramter `haversine=True` or `haversine=T`

It can also compute the adjacent distances for different groups by passing the grouping criteria, `group_by=group`.
This currently supports grouping by a single field. A future update will support grouping by multiple fields.

* Note: The first event in the result will also have a distance of 0.0

* Events that do not have latitudes or longitudes, as is the output when geocoding private non-routed IP addresses,
     will be given a distance of 0.0. The next relative distance will still be based on last public address found.


#### Example 1

This can be used to easily obtain the distance between multiple VPN authentication attempts
which could indicate a compromise where relative distances are above a maximum/expected commutable distance.

```
index=vpn | stats count by src_ip , user |
iplocation src_ip |
fields src_ip, user, lat, lon  |
geodistance latfield=lat longfield=lon output_field=distance group_by=user
```

#### Example 2

This example has been written around the sample app that comes with Splunk.
THis example was carried out using the data generated by the sample app that ships disabled with Splunk Enterprise.

This search extracts the clientip field from the relay field,
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

**Note**: the relative distance between all events with the same clientip will be zero


S3:
```
	index=sample | rex field=relay "\[(?<clientip>.*)\]" |
		iplocation clientip | table clientip lat lon from | search lat=* |
	 	geodistance latfield=lat longfield=lon output_field=distance group_by=from | dedup from distance
```


### Data types

This app outputs the relative distance into the field specified in output_field parameter.


### Configure SA-geodistance

This app has no configurations.

### Troubleshoot SA-geodistance

The command writes logs to `$SPLUNK_HOME/var/log/splunk/SA-geodistance.log```.
This can be seen by searching your internal index using ```index=_internal source=*SA-geodistance.log```.


-- To enable debug logging for the geodistance command, add the following to ```SA-geodistance/local/logging.conf```

```
[logger_GeoDistanceCommand]
level = DEBUG
```


### Upgrade SA-geodistance
This app supports in-place upgrade of older verisons. Alternatively, remove older versions before installing the newest version.


### Copyright & License

#### Copyright - Haversine

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

#### License

This software is licensed under the [Splunk End User License Agreement for Third-Party Content](https://d38o4gzaohghws.cloudfront.net/static/misc/eula.html)
license agreement.
