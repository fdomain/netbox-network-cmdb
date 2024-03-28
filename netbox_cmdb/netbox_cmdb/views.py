"""Views."""

from netbox.views.generic import (
    ObjectDeleteView,
    ObjectEditView,
    ObjectListView,
    ObjectView,
)
from netbox.views.generic.bulk_views import BulkDeleteView
from netbox_cmdb.filtersets import (
    ASNFilterSet,
    BGPPeerGroupFilterSet,
    BGPSessionFilterSet,
    DeviceBGPSessionFilterSet,
)
from netbox_cmdb.forms import (
    ASNForm,
    BGPPeerGroupForm,
    BGPSessionFilterSetForm,
    BGPSessionForm,
    DeviceBGPSessionForm,
)
from netbox_cmdb.models.bgp import ASN, BGPPeerGroup, BGPSession, DeviceBGPSession
from netbox_cmdb.tables import (
    ASNTable,
    BGPPeerGroupTable,
    BGPSessionTable,
    DeviceBGPSessionTable,
)


## ASN views
class ASNListView(ObjectListView):
    queryset = ASN.objects.all()
    filterset = ASNFilterSet
    table = ASNTable
    template_name = "netbox_cmdb/asn_list.html"


class ASNEditView(ObjectEditView):
    queryset = ASN.objects.all()
    form = ASNForm


class ASNDeleteView(ObjectDeleteView):
    queryset = ASN.objects.all()


class ASNView(ObjectView):
    queryset = ASN.objects.all()
    template_name = "netbox_cmdb/asn.html"


## BGP Sessions views


class BGPSessionListView(ObjectListView):
    queryset = BGPSession.objects.prefetch_related("peer_a", "peer_b").all()
    filterset = BGPSessionFilterSet
    filterset_form = BGPSessionFilterSetForm
    table = BGPSessionTable
    template_name = "netbox_cmdb/bgpsession_list.html"


class BGPSessionEditView(ObjectEditView):
    queryset = BGPSession.objects.all()
    form = BGPSessionForm


class BGPSessionBulkDeleteView(BulkDeleteView):
    queryset = BGPSession.objects.all()
    filterset = BGPSessionFilterSet
    table = BGPSessionTable


class BGPSessionDeleteView(ObjectDeleteView):
    queryset = BGPSession.objects.all()


class BGPSessionView(ObjectView):
    queryset = BGPSession.objects.prefetch_related(
        "peer_a", "peer_b", "peer_a__afi_safis", "peer_b__afi_safis"
    ).all()
    template_name = "netbox_cmdb/bgpsession.html"


## DeviceBGPSession views
class DeviceBGPSessionListView(ObjectListView):
    queryset = DeviceBGPSession.objects.all()
    filterset = DeviceBGPSessionFilterSet
    table = DeviceBGPSessionTable


class DeviceBGPSessionView(ObjectView):
    queryset = DeviceBGPSession.objects.all()


class DeviceBGPSessionEditView(ObjectEditView):
    queryset = DeviceBGPSession.objects.all()
    form = DeviceBGPSessionForm
    filterset = DeviceBGPSessionFilterSet


class DeviecBGPSessionDeleteView(ObjectDeleteView):
    queryset = DeviceBGPSession.objects.all()


class DeviecBGPSessionBulkDeleteView(BulkDeleteView):
    queryset = DeviceBGPSession.objects.all()
    filterset = DeviceBGPSessionFilterSet
    table = DeviceBGPSessionTable


## Peer groups views
class BGPPeerGroupListView(ObjectListView):
    queryset = BGPPeerGroup.objects.all()
    filterset = BGPPeerGroupFilterSet
    table = BGPPeerGroupTable
    template_name = "netbox_cmdb/bgppeergroup_list.html"


class BGPPeerGroupEditView(ObjectEditView):
    queryset = BGPPeerGroup.objects.all()
    form = BGPPeerGroupForm


class BGPPeerGroupDeleteView(ObjectDeleteView):
    queryset = BGPPeerGroup.objects.all()


class BGPPeerGroupView(ObjectView):
    queryset = BGPPeerGroup.objects.all()
    template_name = "netbox_cmdb/bgppeergroup.html"
