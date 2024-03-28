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
    RoutePolicyFilterSet,
)
from netbox_cmdb.forms import (
    ASNForm,
    BGPPeerGroupForm,
    BGPSessionFilterSetForm,
    BGPSessionForm,
    DeviceBGPSessionForm,
    RoutePolicyFilterSetForm,
    RoutePolicyForm,
    RoutePolicyTermFormSet,
)
from netbox_cmdb.models.bgp import ASN, BGPPeerGroup, BGPSession, DeviceBGPSession
from netbox_cmdb.models.route_policy import RoutePolicy
from netbox_cmdb.tables import (
    ASNTable,
    BGPPeerGroupTable,
    BGPSessionTable,
    DeviceBGPSessionTable,
    RoutePolicyTable,
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


## Route policy views


class RoutePolicyListView(ObjectListView):
    queryset = RoutePolicy.objects.all()
    filterset_form = RoutePolicyFilterSetForm
    filterset = RoutePolicyFilterSet
    table = RoutePolicyTable


class RoutePolicyView(ObjectView):
    queryset = RoutePolicy.objects.all()
    template_name = "netbox_cmdb/routepolicy.html"


class RoutePolicyEditView(ObjectEditView):
    queryset = RoutePolicy.objects.all()
    form = RoutePolicyForm
    filterset = RoutePolicyFilterSet

    def get(self, request, *args, **kwargs):
        # Get the RoutePolicy instance
        self.object = self.get_object()
        # Initialize the formset with the RoutePolicy instance
        self.term_formset = RoutePolicyTermFormSet(instance=self.object)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Get the RoutePolicy instance
        self.object = self.get_object()
        # Populate the RoutePolicyForm and RoutePolicyTermFormSet with the POST data
        form = self.get_form()
        term_formset = RoutePolicyTermFormSet(request.POST, instance=self.object)
        if form.is_valid() and term_formset.is_valid():
            return self.form_valid(form, term_formset)
        else:
            return self.form_invalid(form, term_formset)

    def form_valid(self, form, term_formset):
        # Save the RoutePolicy instance
        self.object = form.save()
        # Save the related RoutePolicyTerm instances
        term_formset.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the formset to the context
        context["term_formset"] = self.term_formset
        return context


class RoutePolicyDeleteView(ObjectDeleteView):
    queryset = RoutePolicy.objects.all()


class RoutePolicyBulkDeleteView(BulkDeleteView):
    queryset = RoutePolicy.objects.all()
    filterset = RoutePolicyFilterSet
    table = RoutePolicyTable
