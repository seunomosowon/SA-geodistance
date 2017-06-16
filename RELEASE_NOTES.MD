SA-geodistance

This support add-on adds a reporting command to compute the relative vincenty distances of
adjacent events given their latitudes and longitudes.

It computes the distances in miles by default, but this can be made to give results in kilometres.
This can be done by passing `miles=F` as an argument to the command.

It can also compute the adjacent distances for different groups by passing the grouping criteria, `group_by=group`.

This uses the vincenty formula by default, but can be changed to use the haversine's formula instead.
To use haversine instead, add the paramter `haversine=True` or `haversine=T`


## v0.3
- Added support for haversine

## v0.3.1
- Updated check_for_updates in app.conf

## v0.3.3
Fixed logging.conf

## v0.3.4
- Updated permission of files
- Added syntax to search UI

## v0.3.5 / 0.3.6
- Added icons
- called icons to size

## v0.3.7
- Updated field descripition for longitude and haversine
