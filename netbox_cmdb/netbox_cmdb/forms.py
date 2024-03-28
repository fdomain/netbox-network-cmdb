"""Forms."""

from typing import Any, Sequence

from dcim.models import Device
from dcim.models.devices import DeviceType
from dcim.models.sites import Site, SiteGroup
from django import forms
from django.utils.translation import gettext as _
from extras.models import Tag
from utilities.forms import DynamicModelMultipleChoiceField
from utilities.forms.fields import DynamicModelChoiceField, MultipleChoiceField
from utilities.forms.fields.fields import SlugField

from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm
from netbox_cmdb.choices import AssetMonitoringStateChoices, AssetStateChoices
from netbox_cmdb.models.bgp import ASN, BGPPeerGroup, BGPSession, DeviceBGPSession
from netbox_cmdb.models.route_policy import RoutePolicy, RoutePolicyTerm


class ASNForm(NetBoxModelForm):
    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        model = ASN
        fields = ["number", "organization_name", "tags"]


class BGPSessionForm(NetBoxModelForm):
    peer_a = DynamicModelChoiceField(
        queryset=DeviceBGPSession.objects.all(),
        label=_("Peer A"),
        required=True,
    )
    peer_b = DynamicModelChoiceField(
        queryset=DeviceBGPSession.objects.all(),
        label=_("Peer B"),
        required=True,
    )

    class Meta:
        model = BGPSession
        fields = ["peer_a", "peer_b", "state", "monitoring_state", "tenant"]


class DeviceBGPSessionForm(NetBoxModelForm):
    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        initial = kwargs.get("initial", {})
        if instance is not None and instance.device:
            initial["device"] = str(instance.device)
            kwargs["initial"] = initial
        super().__init__(*args, **kwargs)

    device = forms.CharField(disabled=True)
    route_policy_in = DynamicModelChoiceField(
        queryset=RoutePolicy.objects.all(),
        label=_("Route Policy in"),
        query_params={
            "device__id": "$device",
        },
        to_field_name="name",
        fetch_trigger="open",
        required=False,
    )
    route_policy_out = DynamicModelChoiceField(
        queryset=RoutePolicy.objects.all(),
        label=_("Route Policy out"),
        query_params={
            "device__id": "$device",
        },
        to_field_name="name",
        fetch_trigger="open",
        required=False,
    )

    class Meta:
        model = DeviceBGPSession
        fields = ["device", "route_policy_in", "route_policy_out"]


class BGPSessionFilterSetForm(NetBoxModelFilterSetForm):
    device__site__group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        label=_("Site"),
        required=False,
    )
    device__device_type_id = DynamicModelMultipleChoiceField(
        queryset=DeviceType.objects.all(),
        label=_("Device type"),
        required=False,
    )
    state = MultipleChoiceField(choices=AssetStateChoices, required=False)
    monitoring_state = MultipleChoiceField(choices=AssetMonitoringStateChoices, required=False)

    model = BGPSession


class BGPPeerGroupForm(NetBoxModelForm):
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
    )
    device = DynamicModelChoiceField(queryset=Device.objects.all())
    local_asn = DynamicModelChoiceField(queryset=ASN.objects.all(), required=False)
    remote_asn = DynamicModelChoiceField(queryset=ASN.objects.all(), required=False)

    class Meta:
        model = BGPPeerGroup
        fields = [
            "name",
            "device",
            "local_asn",
            "remote_asn",
            "tags",
        ]


class RoutePolicyForm(NetBoxModelForm):
    device = DynamicModelChoiceField(queryset=Device.objects.all())

    class Meta:
        model = RoutePolicy
        fields = [
            "name",
            "device",
            "description",
        ]


RoutePolicyTermFormSet = forms.inlineformset_factory(
    RoutePolicy,  # Parent model
    RoutePolicyTerm,  # Child model
    fields=[
        "description",
        "sequence",
        "decision",
        "from_bgp_community",
        "from_bgp_community_list",
        "from_prefix_list",
        "from_source_protocol",
        "from_route_type",
        "from_local_pref",
        "set_local_pref",
        "set_community",
        "set_origin",
        "set_metric",
        "set_large_community",
        "set_as_path_prepend_asn",
        "set_as_path_prepend_repeat",
        "set_next_hop",
    ],
    extra=1,  # Number of extra forms
)


class RoutePolicyFilterSetForm(NetBoxModelFilterSetForm):
    device__id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        label=_("Device"),
        required=False,
    )
    name = forms.CharField(
        required=False,
    )

    model = RoutePolicy


class InlineTermForm(forms.models.BaseInlineFormSet):
    """InlineTermForm is a form that require at least one item to be valid.
    It is useful for following models:
    - bgp community list
    - route policies
    - prefix list"""

    def clean(self):
        # count valid forms.
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                pass  # such validation is already handled in previous validation steps
        if count < 1:
            raise forms.ValidationError("You must have at least one term.")
