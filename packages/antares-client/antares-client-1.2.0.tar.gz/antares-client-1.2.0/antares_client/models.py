from collections import defaultdict
from typing import List

import astropy.timeseries
import pandas as pd
from astropy.coordinates import SkyCoord

from ._api.api import _get_resource, _list_resources
from ._api.schemas import _AlertSchema, _CatalogEntrySchema, _LocusSchema
from .config import config
from .utils import mjd_to_datetime


class Alert:
    def __init__(self, alert_id: str, mjd: float, properties: dict, **_):
        self.alert_id = alert_id
        self.mjd = mjd
        self.properties = properties


class Locus:
    def __init__(
        self,
        locus_id: str,
        ra: float,
        dec: float,
        properties: dict,
        tags: List[str],
        alerts: List[Alert] = None,
        catalogs: List[str] = None,
        catalog_objects: List[dict] = None,
        lightcurve: pd.DataFrame = None,
        watch_list_ids: List[str] = None,
        watch_object_ids: List[str] = None,
        **_,
    ):
        self.locus_id = locus_id
        self.ra = ra
        self.dec = dec
        self.properties = properties
        self.tags = tags
        self.catalogs = catalogs
        if self.catalogs is None:
            self.catalogs = []
        self.watch_list_ids = watch_list_ids
        if self.watch_list_ids is None:
            self.watch_list_ids = []
        self.watch_object_ids = watch_object_ids
        if self.watch_object_ids is None:
            self.watch_object_ids = []
        self._alerts = alerts
        self._catalog_objects = catalog_objects
        self._lightcurve = lightcurve
        self._timeseries = None
        self._coordinates = None

    def _fetch_alerts(self):
        alerts = _list_resources(
            config["ANTARES_API_BASE_URL"]
            + "/".join(("loci", self.locus_id, "alerts")),
            _AlertSchema,
        )
        return list(alerts)

    def _fetch_lightcurve(self):
        locus = _get_resource(
            config["ANTARES_API_BASE_URL"] + "/".join(("loci", self.locus_id)),
            _LocusSchema,
        )
        return locus.lightcurve

    def _fetch_catalog_objects(self):
        catalog_matches = _list_resources(
            config["ANTARES_API_BASE_URL"]
            + "/".join(("loci", self.locus_id, "catalog-matches")),
            _CatalogEntrySchema,
        )
        catalog_matches = list(catalog_matches)
        catalog_objects = defaultdict(list)
        for match in catalog_matches:
            catalog_name = match["catalog_entry_id"].split(":")[0]
            catalog_objects[catalog_name].append(match["properties"])
        return catalog_objects

    @property
    def timeseries(self):
        if self._timeseries is None:
            self._timeseries = astropy.timeseries.TimeSeries(
                data=[alert.properties for alert in self.alerts],
                time=[mjd_to_datetime(alert.mjd) for alert in self.alerts],
            )
        return self._timeseries

    @timeseries.setter
    def timeseries(self, value):
        self._timeseries = value

    @property
    def alerts(self):
        if self._alerts is None:
            self._alerts = self._fetch_alerts()
        return self._alerts

    @alerts.setter
    def alerts(self, value):
        self._alerts = value

    @property
    def catalog_objects(self):
        if self._catalog_objects is None:
            self._catalog_objects = self._fetch_catalog_objects()
        return self._catalog_objects

    @catalog_objects.setter
    def catalog_objects(self, value):
        self._catalog_objects = value

    @property
    def lightcurve(self):
        if self._lightcurve is None:
            self._lightcurve = self._fetch_lightcurve()
        return self._lightcurve

    @lightcurve.setter
    def lightcurve(self, value):
        self._lightcurve = value

    @property
    def coordinates(self):
        if self._coordinates is None:
            self._coordinates = SkyCoord(f"{self.ra}d {self.dec}d")
        return self._coordinates
