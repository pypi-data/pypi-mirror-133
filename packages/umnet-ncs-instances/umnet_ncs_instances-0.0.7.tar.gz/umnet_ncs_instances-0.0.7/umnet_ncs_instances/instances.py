from .types import *


class NetsplashGetInterfaces(NCSInstance):

    _path = "/action/services/netsplash-get-interfaces"

    _nsmap = {
        "action":"urn:ietf:params:xml:ns:yang:1",
        "services":"http://tail-f.com/ns/ncs",
        "netsplash-get-interfaces":"http://umnet.umich.edu/netsplash",
        }

    def initialize_model(self):

        self.ip_or_name = Choice(['device-hostname','device-ip'])
        self.ip_or_name.device_ip = Leaf(str)
        self.ip_or_name.device_hostname = Leaf(str)

class NetsplashGetSwitchesByZone(NCSInstance):

    _path = "/action/services/netsplash-get-switches-by-zone"

    _nsmap = {
        "action":"urn:ietf:params:xml:ns:yang:1",
        "services":"http://tail-f.com/ns/ncs",
        "netsplash-get-switches-by-zone":"http://umnet.umich.edu/netsplash",
        }

    def initialize_model(self):
        self.zone = Leaf(str)


class NetsplashUpdateInterfaces(NCSInstance):

    _path = "/action/services/netsplash-update-interfaces"

    _nsmap = {
        "action":"urn:ietf:params:xml:ns:yang:1",
        "services":"http://tail-f.com/ns/ncs",
        "netsplash-update-interfaces":"http://umnet.umich.edu/netsplash",
        }

    def initialize_model(self):

        self.switch = Leaf(str)
        self.zone = Leaf(str)
        self.switchport = List(NetsplashSwitchport)


class NetsplashSwitchport(Choice):
    
    def initialize_model(self, choice=None):

        # the choice initializer creates empty containers
        # for 'access' and 'default' for us
        super().__init__(['access','default'])
        
        # now we need to fill in everything else
        self.name = Leaf(str)
        self.access.description = Leaf(str)
        self.access.vlan_name = Leaf(str)
        self.access.admin_status = Leaf(str)
        self.access.voip_enabled = Leaf(bool)

        # can't apply choice until after we've initialized
        # all options!
        if choice:
            self.choose(choice)

class Devices(NCSInstance):

    _path = "/config/devices"

    _nsmap = {
            "config":"http://tail-f.com/ns/config/1.0",
            "devices":"http://tail-f.com/ns/ncs",
            }

    _xml_munge = {
        r'<ned-id>(.+)</ned-id>':'<ned-id xmlns:\g<1>="http://tail-f.com/ns/ned-id/\g<1>">\g<1></ned-id>'
    }

    def initialize_model(self):
        self.device = List(Device)

class Device(NCSInstance):

    _path = "/config/devices/device"

    _nsmap = {
            "config":"http://tail-f.com/ns/config/1.0",
            "devices":"http://tail-f.com/ns/ncs",
            }

    _xml_munge = {
        r'<ned-id>(.+)</ned-id>':'<ned-id xmlns:\g<1>="http://tail-f.com/ns/ned-id/\g<1>">\g<1></ned-id>'
    }

    def initialize_model(self):

        self.name = Leaf(str)
        self.address = Leaf(str)
        self.authgroup = Leaf(str, value="default")
        self.device_role = Leaf(str)
        self.state = Container()
        self.state.admin_state = Leaf(str, value="unlocked")
        self.device_type = Container()
        self.device_type.ned_type = Choice(['cli','netconf'])
        self.device_type.ned_type.cli = Container()
        self.device_type.ned_type.netconf = Container()
        self.device_type.ned_type.cli.ned_id = Leaf(str)
        self.device_type.ned_type.netconf.ned_id = Leaf(str)
        self.in_band_mgmt = Container()
        self.in_band_mgmt.set_ns("http://umnet.umich.edu/umnetcommon")
        self.in_band_mgmt.ip_address = Leaf(str)
        self.in_band_mgmt.interface = Leaf(str)
        self.um_building = Container()
        self.um_building.set_ns("http://umnet.umich.edu/umnetcommon")
        self.um_building.building_no = Leaf(str)
        self.um_building.building_name = Leaf(str)
        self.um_building.building_address = Leaf(str)
        self.um_building.room_no = Leaf(str)


class Switchport(NCSInstance):

    def initialize_model(self):

        self.name = Leaf(str)
        self.enabled = Leaf(bool)
        self.description = Leaf(str)
        self.mode = Container()

        self.mode.mode_choice = Choice(['access','trunk','default'])
        self.mode.mode_choice.access = Container()
        self.mode.mode_choice.access.vlan = Leaf(str)
        self.mode.mode_choice.access.voip_enabled = Leaf(bool, value=False)
        self.mode.mode_choice.trunk = Container()
        self.mode.mode_choice.trunk.native_vlan = Leaf(str)
        self.mode.mode_choice.trunk.vlan_list = LeafList(str)
        self.mode.mode_choice.default = Container()

class Network(NCSInstance):

    _path = "/config/services/network"
    _nsmap = {
            "config":"http://tail-f.com/ns/config/1.0",
            "services":"http://tail-f.com/ns/ncs",
            "network":"http://example.com/umnet-network",
            }

    def initialize_model(self):

        self.name = Leaf(str)
        self.role = Leaf(str)
        self.description = Leaf(str)
        self.layer2 = Container()
        self.layer2.vlan_id = Leaf(int)

        self.layer3 = Container()
        self.layer3.vrf = Leaf(str)
        self.layer3.primary_ipv4_subnet = Leaf(str)
        self.layer3.secondary_ipv4_subnets = LeafList(str)
        self.layer3.ipv6_subnet = LeafList(str)
        self.layer3.dhcp_relay_servers = Leaf(str)
        self.layer3.ingress_acl = Leaf(str)
        self.layer3.egress_acl = Leaf(str)

class Networks(NCSInstance):

    _path = "/config/services"
    _nsmap = {
            "config":"http://tail-f.com/ns/config/1.0",
            "services":"http://tail-f.com/ns/ncs",
            }

    def initialize_model(self):

        self.network = List(Network)
        self.network.set_ns("http://example.com/umnet-network")

class NGFWVsyses(NCSInstance):
    _path = "/config/services"
    _nsmap = {
            "config":"http://tail-f.com/ns/config/1.0",
            "services":"http://tail-f.com/ns/ncs",
            }
    def initialize_model(self):
        self.ngfw_vsys = List(NGFWVsys)
        sels.ngfw_vsys.set_ns("http://umnet.umich.edu/umnet-vrf")

class NGFWVsys(NCSInstance):

    def initialize_model(self):
        self.name = Leaf('str')
        self.asn = Leaf('str')
        
class Vrf(NCSInstance):

    def initialize_model(self):

        self.name = Leaf('str')
        self.ngfw_vsys_or_vrf_asn = Choice(['ngfw-vsys', 'vrf-asn'])
        self.ngfw_vsys_or_vrf_asn.ngfw_vsys = Leaf(str)
        self.ngfw_vsys_or_vrf_asn.vrf_asn = Leaf(int)

        self.vrf_no = Leaf(int)

class Vrfs(NCSInstance):

    _path = "/config/services"
    _nsmap = {
            "config":"http://tail-f.com/ns/config/1.0",
            "services":"http://tail-f.com/ns/ncs",
            }

    def initialize_model(self):
        self.vrf = List(Vrf)
        self.vrf.set_ns('http://umnet.umich.edu/umnet-vrf')

class BaseconfProfile(NCSInstance):
    '''
    For the ncs migration project we don't actually
    profiles, we just need to be able to add devices to
    ones that already exist. As a result we're not defining
    any groups or profile details here.
    '''

    def initialize_model(self):
        self.name = Leaf('str')
        self.devices = LeafList('str')


class Baseconf(NCSInstance):
    _path = "/config/services/baseconf"
    _nsmap = {
            "config":"http://tail-f.com/ns/config/1.0",
            "services":"http://tail-f.com/ns/ncs",
            "baseconf":"http://umnet.umich.edu/umnet-baseconf",
            }

    def initialize_model(self):
        self.profile = List(BaseconfProfile)



class Switch(NCSInstance):

    def initialize_model(self):
        self.name = Leaf(str)
        self.switchport = List(Switchport)

class SwitchUplinks(NCSInstance):
    def initialize_model(self):
        self.name = Leaf(str)
        self.uplink = List(Uplink)

class Uplink(NCSInstance):

    def initialize_model(self):
        self.name = Leaf(str)
        self.uplink_type = Choice(['single-dl','al-to-al'])
        self.uplink_type.single_dl = Container()
        self.uplink_type.single_dl.pri_or_sec = Choice(['primary','secondary'])
        self.uplink_type.single_dl.pri_or_sec.primary = Container()
        self.uplink_type.single_dl.pri_or_sec.primary.primary_router_ifname = Leaf(str)
        self.uplink_type.single_dl.pri_or_sec.secondary = Container()
        self.uplink_type.single_dl.pri_or_sec.secondary.secondary_router_ifname = Leaf(str)

        self.uplink_type.al_to_al = Container()
        self.uplink_type.al_to_al.remote_switch = Leaf(str)
        self.uplink_type.al_to_al.remote_interface = Leaf(str)


class Distribution(NCSInstance):

    _path = "/config/services/distribution"
    _nsmap = {
            "config":"http://tail-f.com/ns/config/1.0",
            "services":"http://tail-f.com/ns/ncs",
            "distribution":"http://umnet.umich.edu/distribution",
            }


    def initialize_model(self):
    
        self.name = Leaf(str)
        self.legacy_zone = Leaf(bool, True)
        self.fabric = Leaf(str)

        self.routing = Container()
        self.routing.network = LeafList(str)

        # note that because we're only dealing with legacy zones
        # right now, the primary/secondary DLs can be modeled
        # as switches.
        self.routing.primary_router = Switch()
        self.routing.secondary_router = Switch()

        self.switch = List(Switch)

        self.uplinks = Container()
        self.uplinks.switch = List(SwitchUplinks)

class DHCPServerGroup(NCSInstance):

    def initialize_model(self):
        self.name = Leaf(str)
        self.server_ip = LeafList(str)

class Constants(NCSInstance):
    _path = "/config/services/constants/dhcp-server-group"
    _nsmap = {
            "config":"http://tail-f.com/ns/config/1.0",
            "services":"http://tail-f.com/ns/ncs",
            "constants":"http://umnet.umich.edu/constants",
    }

    def initialize_model(self):
        self.dhcp_server_group = List(DHCPServerGroup)

