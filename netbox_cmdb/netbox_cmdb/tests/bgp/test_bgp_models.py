from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from django.db.models import RestrictedError
from django.test import TestCase
from ipam.models.ip import IPAddress
from tenancy.models.tenants import Tenant

from netbox_cmdb.models import ASN, BGPPeerGroup, BGPSession, DeviceBGPSession
from netbox_cmdb.models.route_policy import RoutePolicy


class BGPSessionDeleteCascadeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        site = Site.objects.create(name="SiteTest", slug="site-test")
        manufacturer = Manufacturer.objects.create(name="test", slug="test")
        device_type = DeviceType.objects.create(
            manufacturer=manufacturer, model="model-test", slug="model-test"
        )
        device_role = DeviceRole.objects.create(name="role-test", slug="role-test")
        cls.devices = [
            Device(name="router1", device_role=device_role, device_type=device_type, site=site),
            Device(name="router2", device_role=device_role, device_type=device_type, site=site),
            Device(name="router3", device_role=device_role, device_type=device_type, site=site),
        ]
        Device.objects.bulk_create(cls.devices)

        tenants = [
            Tenant(name="tenant1", slug="tenant1"),
            Tenant(name="tenant2", slug="tenant2"),
            Tenant(name="tenant3", slug="tenant3"),
        ]
        Tenant.objects.bulk_create(tenants)

        asns = [
            ASN(number="1", organization_name="router1"),
            ASN(number="2", organization_name="router2"),
            ASN(number="3", organization_name="router3"),
        ]
        ASN.objects.bulk_create(asns)

        ip_addresses = [
            IPAddress(address="10.0.0.1/32"),
            IPAddress(address="10.0.0.2/32"),
            IPAddress(address="10.0.0.3/32"),
        ]
        IPAddress.objects.bulk_create(ip_addresses)

        bgp_peer_groups = [
            BGPPeerGroup(name="PG-TEST", device=cls.devices[0]),
            BGPPeerGroup(name="PG-TEST", device=cls.devices[1]),
            BGPPeerGroup(name="PG-TEST", device=cls.devices[2]),
        ]
        BGPPeerGroup.objects.bulk_create(bgp_peer_groups)

        route_policies = [
            RoutePolicy(device=cls.devices[0], name="RM-TEST"),
            RoutePolicy(device=cls.devices[1], name="RM-TEST"),
            RoutePolicy(device=cls.devices[2], name="RM-TEST"),
        ]
        RoutePolicy.objects.bulk_create(route_policies)

        device_bgp_sessions = [
            DeviceBGPSession(
                device=cls.devices[0],
                local_address=ip_addresses[0],
                peer_group=bgp_peer_groups[0],
                route_policy_in=route_policies[0],
            ),
            DeviceBGPSession(
                device=cls.devices[0],
                local_address=ip_addresses[0],
                peer_group=bgp_peer_groups[0],
                route_policy_in=route_policies[0],
            ),
            DeviceBGPSession(
                device=cls.devices[1],
                local_address=ip_addresses[1],
                peer_group=bgp_peer_groups[1],
                route_policy_in=route_policies[1],
            ),
            DeviceBGPSession(
                device=cls.devices[1],
                local_address=ip_addresses[1],
                peer_group=bgp_peer_groups[1],
                route_policy_in=route_policies[1],
            ),
            DeviceBGPSession(
                device=cls.devices[2],
                local_address=ip_addresses[2],
                peer_group=bgp_peer_groups[2],
                route_policy_in=route_policies[2],
            ),
            DeviceBGPSession(
                device=cls.devices[2],
                local_address=ip_addresses[2],
                peer_group=bgp_peer_groups[2],
                route_policy_in=route_policies[2],
            ),
        ]
        DeviceBGPSession.objects.bulk_create(device_bgp_sessions)

        bgp_sessions = [
            BGPSession(
                state="production",
                peer_a=device_bgp_sessions[0],
                peer_b=device_bgp_sessions[2],
                tenant=tenants[0],
            ),
            BGPSession(
                state="production",
                peer_a=device_bgp_sessions[1],
                peer_b=device_bgp_sessions[4],
                tenant=tenants[1],
            ),
            BGPSession(
                state="production",
                peer_a=device_bgp_sessions[3],
                peer_b=device_bgp_sessions[5],
                tenant=tenants[2],
            ),
        ]
        BGPSession.objects.bulk_create(bgp_sessions)

    def test_delete_device(self):
        # we delete the first device, it is supposed to remove all related BGP objects
        self.devices[0].delete()
        # we are supposed to have only 1 bgp session left (between router 2 and router 3)
        bgp_session = BGPSession.objects.all()
        # objects like RoutePolicies
        self.assertEqual(len(bgp_session), 1)

    def test_delete_route_policy__restricted(self):
        # try to delete a routing policy currently used by on a DeviceBGPSession
        rp = RoutePolicy.objects.all().first()
        # it must raise a RestrictedError as the object is used
        self.assertRaises(RestrictedError, rp.delete)

    def test_delete_device_bgp_peergroup__restricted(self):
        # try to delete a bgp peer group currently used by on a DeviceBGPSession
        bgp_peer_group = BGPPeerGroup.objects.all().first()
        # it must raise a RestrictedError as the object is used
        self.assertRaises(RestrictedError, bgp_peer_group.delete)

    def test_delete_device_bgp_session__ok(self):
        device_bgp_session = DeviceBGPSession.objects.all().first()
        print(device_bgp_session)
        device_bgp_session.delete()
        print(len(BGPSession.objects.all()))

    def test_delete_bgp_session(self):
        # removing a BGP session must remove related DeviceBGPsession objects, but not RoutePolicy or other
        # objects that may be used somewhere else
        bgp_session = BGPSession.objects.all().first()
        bgp_session.delete()
        rp_peer_a = RoutePolicy.objects.filter(device=bgp_session.peer_a.device)
        rp_peer_b = RoutePolicy.objects.filter(device=bgp_session.peer_b.device)
        self.assertEqual(len(rp_peer_a), 1)
        self.assertEqual(len(rp_peer_b), 1)
