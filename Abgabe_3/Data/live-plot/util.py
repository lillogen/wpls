import time

from Channel import Channel, MeasurementChannel

unit = {
    'RSSI': 'dBm',
    'TIME': 's'
}


def timestamp():
    """
    Gets the current timestamp in millisecond resolution
    :return: timestamp with millisecond resolution
    """
    return float(time.time())


class GraphPoint:
    def __init__(self, index, name, x, y):
        """
        Creates a GraphPoint instance
        :param index: index of the plot to be used
        :param name: name of the graph this point is appended
        :param x: x coordinate
        :param y: y coordinate
        """
        self.index = index
        self.name = name
        self.x = x
        self.y = y


def get_channel(channels, fro, to, me, create=False):
    """
    Returns a channel from the list matching the given parameters
    :param channels: list of Channel objects
    :type channels: list()
    :param fro: from address
    :param to: to address
    :param me: me address
    :param create: create a new channel (MeasurementChannel) if it doesnt exist yet
    :rtype: Channel
    :return Matching channel or None
    """
    for candidate in channels:
        assert isinstance(candidate, Channel)
        if candidate.fro == fro and candidate.to == to and candidate.me == me:
            return candidate
    if create:
        channel = MeasurementChannel(fro, to, me)
        channels.append(channel)
        return channel
    return None


def get_partner_channel(channels, channel):
    """
    Returns the partner channel

    :param channels: List of all channels
    :param channel: The channel whose partner is to be found
    :return: the partner channel
    """
    if channel.to != channel.me:
        # This is a sniffer
        return get_channel(channels, channel.to, channel.fro, channel.me, False)
    else:
        # This is a regular channel
        return get_channel(channels, channel.to, channel.fro, channel.fro, False)
