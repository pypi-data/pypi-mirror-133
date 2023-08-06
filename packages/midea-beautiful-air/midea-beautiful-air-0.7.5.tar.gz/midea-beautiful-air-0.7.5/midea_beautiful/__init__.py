""" Library for local network access to Midea dehumidifier appliances """
from __future__ import annotations

from midea_beautiful.version import __version__
from midea_beautiful.cloud import MideaCloud
from midea_beautiful.lan import LanDevice, get_appliance_state
from midea_beautiful.midea import DEFAULT_APP_ID, DEFAULT_APPKEY
from midea_beautiful.scanner import find_appliances

__version__ = __version__


def discover_appliances(
    appkey: str = DEFAULT_APPKEY,
    account: str = None,
    password: str = None,
    appid: int = DEFAULT_APP_ID,
    cloud: MideaCloud | None = None,
    networks: list[str] = [],
) -> list[LanDevice]:
    """
    Discovers appliances on local network

    Args:
        appkey (str, optional): Midea app application key. If not
            provided, cloud interface must be provided and will
            be used to discover appliance information and token.
            Defaults to None.
        account (str, optional): Midea app user e-mail. If not
            provided, cloud interface must be provided and will
            be used to discover appliance information and token.
            Defaults to None.
        password (str, optional): Midea app password. If not
            provided, cloud interface must be provided and will
            be used to discover appliance information and token.
            Defaults to None.
        cloud (MideaCloud, optional): Interface to Midea cloud API.
            Used when credentials were not provided. Defaults to None.
        broadcast_retries (int, optional): Number of retries for UDP
            broadcast. Defaults to 2.

    Returns:
        list[LanDevice]: List of appliances. Appliances that
            are found via Midea cloud API, but are not discovered will
            have IP address set to None.
    """
    return find_appliances(cloud, appkey, account, password, str(appid), networks)


def appliance_state(
    ip: str | None = None,
    token: str | None = None,
    key: str | None = None,
    cloud: MideaCloud = None,
    use_cloud: bool = False,
    id: str | None = None,
) -> LanDevice | None:
    """
    Retrieves appliance state

    Args:
        ip (str): IP address of the appliance
        token (str, optional): Token used to connect to
            appliance on local network. If not provided, cloud
            interface must be provided and will be used
            to discover token. Defaults to None.
        key (str, optional): Key for token. If not provided, cloud
            interface must be provided and will be used
            to discover token. Defaults to None.
        cloud (MideaCloud, optional): Interface to Midea cloud API.
            Used to discover token if it was not provided in arguments.
            Defaults to None.
        use_cloud (bool, optional): Set to True if state should be
            retrieved from cloud.

    Returns:
        LanDevice: Appliance descriptor and state
    """
    return get_appliance_state(
        ip=ip, token=token, key=key, cloud=cloud, use_cloud=use_cloud, id=id
    )


def connect_to_cloud(
    account: str, password: str, appkey=DEFAULT_APPKEY, appid=DEFAULT_APP_ID
) -> MideaCloud:
    """
    Connects to Midea cloud API

    Args:
        appkey (str): Midea app key
        account (str): Midea app user e-mail
        password (str): Midea app password
        appid (str): Midea app id

    Returns:
        MideaCloud: Interface to Midea cloud API
    """
    cloud = MideaCloud(appkey, account, password, appid)
    cloud.authenticate()
    return cloud
