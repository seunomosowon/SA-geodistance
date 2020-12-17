import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from splunklib.searchcommands import dispatch, ReportingCommand, Configuration, Option, validators
from vincenty import vincenty
from haversine import haversine, Unit
from splunklib.searchcommands import environment


@Configuration()
class GeoDistanceCommand(ReportingCommand):
    """ Computes the distance of adjacent events

    ##Syntax

    .. code-block::
        geodistance latfield=<field> longfield=<field> output_field=<field> miles=<bool> group_by=field_to_group_by
                    haversine=<bool>

    ##Description

    This search command calculates the relative vincenty distances of adjacent events given their coordinates
    (latitudes and longitudes).
    It computes the distances in miles by default, but changed to Km by setting `miles=F`
    It can also compute the adjacent distances for a groups when the `group_by` is specified.

    ##Note:

    *Events that do not have latitudes or longitudes, as is the output when geocoding private non-routable IP addresses,
     will be given a distance of 0.0. The next relative distance will still be based on last public address found.

    *The first event in the result will also have a distance of 0.0

    ##Example

    This example computes the relative distance for adjacent VPN connection attempts made by each user

    CLI:
    ..code-block::
            "index=vpn | stats count by src_ip , user |
             iplocation src_ip | fields src_ip, user, lat, lon  |
             geodistance latfield=lat longfield=lon output_field=distance miles=F
             group_by=user haversine=False"

    """
    latfield = Option(
        doc='''
        **Syntax:** **latfield=** *<fieldname>*
        **Description:** Name of the field that holds the latitude''',
        require=True, validate=validators.Fieldname())
    longfield = Option(
        doc='''
        **Syntax:** **longfield=** *<fieldname>*
        **Description:** Name of the field that holds the longitude''',
        require=True, validate=validators.Fieldname())
    group_by = Option(
        doc='''
        **Syntax:** **group_by=** *<fieldname>*
        **Description:** Name of the field to be used to categorize events when computing distances''',
        require=False, validate=validators.Fieldname())
    miles = Option(
        doc='''
        **Syntax:** **miles=** *<bool>*
        **Description:** If set to true, this converts the distance to miles instead of km''',
        require=False, validate=validators.Boolean(), default=False)
    output_field = Option(
        doc='''
        **Syntax:** **output_field=** *<fieldname>*
        **Description:** Name of the field that will hold the relative distance returned in the output''',
        require=True, validate=validators.Fieldname())
    use_haversine = Option(
        name='haversine',
        doc='''
        **Syntax:** **haversine=** *<fieldname>*
        **Description:** If set to true, this calculates the harversine distance instead of the vincenty distance''',
        require=False, validate=validators.Boolean(), default=False)

    def __init__(self):
        super(GeoDistanceCommand, self).__init__()
        environment.splunklib_logger = self._logger

    @Configuration()
    def map(self, events):
        for event in events:
            yield event

    def reduce(self, events):
        latitude = self.latfield
        longitude = self.longfield
        relative_distance = self.output_field
        use_haversine = bool(self.use_haversine)
        self.logger.info("[%s] - Starting geodistance instance" % str(self.metadata.searchinfo.sid))
        self.logger.debug("[%s] - Using parameters - %s" % (str(self.metadata.searchinfo.sid), str(self.metadata)))
        haversine_unit = Unit.MILES if self.miles else Unit.KILOMETERS
        if self.group_by:
            position_tracker = {}
            for event in events:
                current = event
                if not (current[latitude] or current[longitude]):
                    current[relative_distance] = 0.0
                    self.logger.debug("[%s] - Using distance=0 for private IPs or unknown coordinates. "
                                      "Exclude if undesired." % str(self.metadata.searchinfo.sid))
                else:
                    current_pos = (float(current[latitude]), float(current[longitude]))
                    if current[self.group_by] not in position_tracker.keys():
                        last_pos = None
                    else:
                        last_pos = position_tracker[current[self.group_by]]
                    if last_pos is None:
                        current[relative_distance] = 0.0
                        self.logger.debug(
                            "[%s] - Initializing the first location with distance=0" % str(self.metadata.searchinfo.sid)
                        )
                    else:
                        if use_haversine:
                            current[relative_distance] = haversine(last_pos, current_pos, unit=haversine_unit)
                        else:
                            current[relative_distance] = vincenty(last_pos, current_pos, miles=bool(self.miles))
                    position_tracker[current[self.group_by]] = current_pos
                yield current
        else:
            last_pos = None
            for event in events:
                current = event
                if not (current[latitude] or current[longitude]):
                    current[relative_distance] = 0.0
                    self.logger.debug(
                        "[%s] - Using distance=0 for private IPs or unknown coordinates. Exclude if undesired." % str(
                            self.metadata.searchinfo.sid))
                else:
                    current_pos = (float(current[latitude]), float(current[longitude]))
                    if last_pos is None:
                        current[relative_distance] = 0.0
                        self.logger.debug("[%s] - Initializing the first location with distance=0" % str(
                            self.metadata.searchinfo.sid))
                    else:
                        if use_haversine:
                            current[relative_distance] = haversine(last_pos, current_pos, unit=haversine_unit)
                        else:
                            current[relative_distance] = vincenty(last_pos, current_pos, miles=self.miles)
                    last_pos = current_pos
                self.logger.debug(current)
                yield current
            self.logger.info("[%s] - Completed successfully." % str(self.metadata.searchinfo.sid))


dispatch(GeoDistanceCommand, sys.argv, sys.stdin, sys.stdout, __name__)
