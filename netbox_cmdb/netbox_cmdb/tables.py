"""Tables."""

import django_tables2 as tables

from netbox.tables import NetBoxTable, columns
from netbox_cmdb.models.bgp import ASN, BGPPeerGroup, BGPSession, DeviceBGPSession
from netbox_cmdb.models.route_policy import RoutePolicy


class ASNTable(NetBoxTable):
    number = tables.LinkColumn()
    organization_name = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = ASN
        fields = ("pk", "number", "organization_name")


class BGPSessionTable(NetBoxTable):
    id = tables.Column(linkify=True)
    peer_a__device = tables.Column(verbose_name="Device A")
    peer_a__description = tables.Column(verbose_name="Device A description")
    peer_a__local_address = tables.Column(verbose_name="Device A local address")
    peer_b__device = tables.Column(verbose_name="Device B")
    peer_b__description = tables.Column(verbose_name="Device B description")
    peer_b__local_address = tables.Column(verbose_name="Device B local address")
    state = columns.ChoiceFieldColumn()
    monitoring_state = columns.ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = BGPSession
        fields = (
            "id",
            "peer_a__device",
            "peer_a__description",
            "peer_a__local_address",
            "peer_b__device",
            "peer_b__description",
            "peer_b__local_address",
            "state",
            "monitoring_state",
        )


class DeviceBGPSessionTable(NetBoxTable):
    id = tables.Column()
    device = tables.Column(verbose_name="Device")
    description = tables.Column(verbose_name="Description")
    local_address = tables.Column(verbose_name="Local address")
    local_asn = tables.Column(verbose_name="Local ASN")
    route_policy_in = tables.Column(verbose_name="Route Policy in")
    route_policy_out = tables.Column(verbose_name="Route Policy out")
    maximum_prefixes = tables.Column(verbose_name="Maximum prefixes")

    class Meta(NetBoxTable.Meta):
        model = DeviceBGPSession
        fields = (
            "id",
            "device",
            "description",
            "local_address",
            "local_asn",
            "route_policy_in",
            "route_policy_out",
            "maximum_prefixes",
        )


class BGPPeerGroupTable(NetBoxTable):
    device = tables.LinkColumn()
    name = tables.LinkColumn()
    asn = tables.Column()
    route_policy_in = tables.Column()
    route_policy_out = tables.Column()
    maximum_prefixes = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = BGPPeerGroup
        fields = (
            "pk",
            "name",
            "local_asn",
            "remote_asn",
            "route_policy_in",
            "route_policy_out",
            "maximum_prefixes",
        )


class RoutePolicyTable(NetBoxTable):
    device = tables.LinkColumn()
    name = tables.LinkColumn()

    class Meta(NetBoxTable.Meta):
        model = RoutePolicy
        fields = (
            "pk",
            "device",
            "name",
        )
