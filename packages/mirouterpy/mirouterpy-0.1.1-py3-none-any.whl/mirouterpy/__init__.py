import requests

from . import utils

PORTFORWARD_SINGLE = 1
PORTFORWARD_RANGE = 2
UDP = 1
TCP = 2
UDPTCP = 3

FIRMWARE_CHANNELS = {
    'current': 'Beta',
    'release': 'Release',
    'stable': 'Beta'
}
MODELS = {
    'R1D': 'Mi Router',
    'R2D': 'Mi Router 2',
    'R3D': '小米路由器HD',
    'R1CM': 'Mi Router Mini',
    'R1CL': 'Mi Wi-Fi Nano',
    'R3': '小米路由器3',
    'R3L': '小米路由器3C',
    'R3P': '小米路由器3 Pro',
    'R3A': '小米路由器3A',
    'R3G': '小米路由器3G',
    'R4': 'Mi Wi-Fi 4',
    'R4C': '小米路由器4Q',
    'R4CM': 'Mi Wi-Fi 4C',
    'D01': '小米路由器Mesh',
    'R4AC': 'Mi Router 4A',
    'R4A': 'Mi Router 4A Giga Version',
    'R3Gv2': '小米路由器3G',
    'R2600': '小米路由器2600',
    'R2100': '小米路由器2100',
    'R1500': '小米路由器1500',
    'R3600': '小米AIoT路由器 AX3600',
    'RM1800': 'Redmi路由器 AX1800',
    'R2350': 'Mi AIoT Router AC2350',
}

CONNECTION_TYPE = ["Lan", "2.4Ghz", "5Ghz"]


class InvalidTokenException(Exception):
    pass


class MiRouter:
    def __init__(self, address="http://router.miwifi.com", mirouter_type=0):
        if address.endswith("/"):
            address = address[:-1]
        self.address = address
        self.token = None
        self.mirouter_type = mirouter_type
        self._session = requests.Session()

    def login(self, password):
        nonce = utils.generate_nonce(self.mirouter_type)
        data = {
            "username": "admin",
            "nonce": nonce,
            "logtype": "2",
            "password": utils.generate_password_hash(nonce, password),
        }
        response = requests.post(f"{self.address}/cgi-bin/luci/api/xqsystem/login", data=data)

        if response.status_code == 200:
            self.token = response.json()["token"]
        else:
            raise Exception("Login failed.Maybe check your password or router address.")

        return response

    def get_api_endpoint(self, endpoint):
        response = self._session.get(f"{self.address}/cgi-bin/luci/;stok={self.token}/api/{endpoint}")
        data = response.json()
        if response.status_code == 200 and data['code'] != 401:
            return response.json()
        else:
            raise InvalidTokenException(data['msg'])

    def post_api_endpoint(self, endpoint, data):
        response = self._session.post(f"{self.address}/cgi-bin/luci/;stok={self.token}/api/{endpoint}", data=data)
        data = response.json()
        if response.status_code == 200 and data['code'] != 401:
            return response.json()
        else:
            raise InvalidTokenException(data['msg'])

    def logout(self):
        return self.get_api_endpoint("web/logout")

    def reboot(self):
        # reboot router
        return self.get_api_endpoint("xqsystem/reboot")

    def shutdown(self):
        # shutdown router
        return self.get_api_endpoint("xqsystem/shutdown")

    def reset(self):
        # FACTORY RESET ROUTER
        return self.get_api_endpoint("xqsystem/reset")

    def messages(self):
        # messages router needs to  tell you
        return self.get_api_endpoint("misystem/messages")

    def status(self):
        return self.get_api_endpoint("misystem/status")

    def device_list(self):
        return self.get_api_endpoint("misystem/devicelist")

    def bandwidth_test(self, history=None):
        endpoint_url = "misystem/bandwidth_test"
        if history:
            endpoint_url += f"?history={history}"
        return self.get_api_endpoint(endpoint_url)

    def pppoe_status(self):
        return self.get_api_endpoint("xqnetwork/pppoe_status")

    def wifi_detail_all(self):
        return self.get_api_endpoint("xqnetwork/wifi_detail_all")

    def country_code(self):
        return self.get_api_endpoint("xqsystem/country_code")

    def wan_info(self):
        # doesnt work on 4a gigabit
        return self.get_api_endpoint("xqsystem/wan_info")

    def check_wan_type(self):
        # doesnt work on 4a gigabit
        return self.get_api_endpoint("xqsystem/check_wan_type")

    def new_status(self):
        return self.get_api_endpoint("misystem/newstatus")

    def qos_info(self):
        return self.get_api_endpoint("misystem/qos_info")

    def wifi_share_info(self):
        # Guest WiFi info
        return self.get_api_endpoint("misns/wifi_share_info")

    def wifi_macfilter_info(self):
        # TODO: model?
        return self.get_api_endpoint("xqnetwork/wifi_macfilter_info")

    def lan_dhcp(self):
        return self.get_api_endpoint("xqnetwork/lan_dhcp")

    def lan_info(self):
        return self.get_api_endpoint("xqnetwork/lan_info")

    def check_rom_update(self):
        return self.get_api_endpoint("xqsystem/check_rom_update")

    def get_languages(self):
        return self.get_api_endpoint("xqsystem/get_languages")

    def get_location(self):
        return self.get_api_endpoint("xqsystem/get_location")

    def sys_time(self):
        return self.get_api_endpoint("misystem/sys_time")

    def mac_bind_info(self):
        return self.get_api_endpoint("xqnetwork/macbind_info")

    def ddns(self):
        return self.get_api_endpoint("xqnetwork/ddns")

    def portforward(self, type):
        # PORTFORWARD_SINGLE or PORTFORWARD_RANGE
        return self.get_api_endpoint(f"xqnetwork/portforward?ftype={type}")

    def dmz(self):
        return self.get_api_endpoint("xqnetwork/dmz")

    def vpn(self):
        # return VPN configurations
        # has a "list" in which there is an array of dicts
        # each dict has:
        # username|onname|id|proto|password|server
        # id is used to enable/disable vpn + delete
        return self.get_api_endpoint("xqsystem/vpn")

    def smartvpn_info(self):
        return self.get_api_endpoint("misystem/smartvpn_info")

    def mi_vpn_info(self):
        return self.get_api_endpoint("misystem/mi_vpn_info")

    def vpn_status(self):
        return self.get_api_endpoint("xqsystem/vpn_status")

    def upnp(self):
        return self.get_api_endpoint("xqsystem/upnp")

    def sys_log(self):
        # returns "path" and you can download a zip file containing different types of logs from router from that path
        return self.get_api_endpoint("misystem/sys_log")

    def c_backup(self, backup):
        # TODO:parameters?
        return self.get_api_endpoint(
            "misystem/c_backup?keys=mi_basic_info%2Cmi_network_info%2Cmi_wifi_info%2Cmi_lan_info%2Cmi_arn_info")

    def router_name(self):
        # returns router name(set differently than ssid)
        # used in mesh systems to identify router
        return self.get_api_endpoint("misystem/router_name")

    def r_ip_conflict(self):
        # check if there is an ip conflict
        return self.get_api_endpoint("misystem/r_ip_conflict")

    def netspeed(self):
        # speed test
        # seems to give correct bandwidth and download speed. bandwidth_test with history gets stast from this api
        return self.get_api_endpoint("xqnetdetect/netspeed")

    ###POST/SET requests
    def set_band(self, manual, upload, download):
        # set QOS manual bandwidth
        # upload and download are in megabit per second

        data = {"manual": manual,
                "upload": upload,
                "download": download}
        return self.post_api_endpoint("misystem/set_band", data=data)

    def set_mac_filter(self, mac_address, enable):
        # disable or enable "internet access" for a mac address
        return self.get_api_endpoint(f"xqsystem/set_mac_filter?mac={mac_address}&wan={enable}")

    def set_all_wifi(self, band_steering, w24on, w24ssid, w24encryption, w24channel,
                     w24bandwidth, w24hidden, w24txpwr, w24password,
                     w5on=None, w5ssid=None, w5encryption=None, w5channel=None,
                     w5bandwidth=None, w5hidden=None, w5txpwr=None, w5password=None, ):
        # bsd is band steering.if is 0 then ssid2 and other info should be provided.
        # it is recommended to set 5ghz seprately then set bsd to 1

        # bsd=0&on1=1&ssid1=ssidhere&encryption1=mixed-psk&channel1=1&bandwidth1=20&hidden1=0&txpwr1=max&pwd1=passwordssidhere&on2=1&
        #       ssid2=ssidhere&encryption2=mixed-psk&channel2=161&bandwidth2=80&hidden2=0&txpwr2=max&pwd2=passwordssidhere
        #
        # bsd=1&on1=1&ssid1=ssidhere&encryption1=mixed-psk&channel1=1&bandwidth1=20&hidden1=0&txpwr1=max&pwd1=passwordssidhere
        data = {"bsd": band_steering,
                "on1": w24on,
                "ssid1": w24ssid,
                "encryption1": w24encryption,
                "channel1": w24channel,
                "bandwidth1": w24bandwidth,
                "hidden1": w24hidden,
                "txpwr1": w24txpwr,
                "pwd1": w24password,
                }
        if not band_steering:
            data2 = {
                "on2": w5on,
                "ssid2": w5ssid,
                "encryption2": w5encryption,
                "channel2": w5channel,
                "bandwidth2": w5bandwidth,
                "hidden2": w5hidden,
                "txpwr2": w5txpwr,
                "pwd2": w5password,
            }
            data.update(data2)
        return self.post_api_endpoint("xqnetwork/set_all_wifi", data=data)

    def set_wan(self, wan_type, autoset=1, dns1=None, dns2=None):
        # type : dhcp
        data = {"wanType": wan_type,
                "autoset": autoset,
                "dns1": dns1,
                "dns2": dns2,
                }
        return self.post_api_endpoint("xqnetwork/set_wan", data=data)

    def set_wan_speed(self, speed=0):
        # set LAN Speed Auto/100M/1000M
        # set 0 for auto
        data = {"speed": speed}
        return self.post_api_endpoint("xqnetwork/set_wan_speed", data=data)

    def mac_clone(self, mac):
        # clone router mac address
        return self.get_api_endpoint(f"xqnetwork/mac_clone?mac={mac}")

    def wifi_macfilter_info(self):
        return self.get_api_endpoint("xqnetwork/wifi_macfilter_info")

    def edit_device(self, mac, model, options):
        # TODO:parameters?
        raise NotImplementedError
        pass

    def set_wifi_macfilter(self, model, enable):
        # TODO:parameters?
        raise NotImplementedError
        pass

    def set_name_password(self, new_password, old_password):
        # nonce=random_nonce&newPwd=newpasshash&oldPwd=oldpasshash
        nonce = utils.generate_nonce(self.mirouter_type)
        new_password = utils.generate_password_hash(nonce, new_password)
        old_password = utils.generate_password_hash(nonce, old_password)
        data = {"nonce": nonce,
                "newPwd": new_password,
                "oldPwd": old_password,
                }
        return self.post_api_endpoint("xqsystem/set_name_password", data=data)

    def web_access_opt(self, open):
        # set web admin access on/off:1/0
        data = {"open": open}
        return self.post_api_endpoint("misystem/web_access_opt", data=data)

    def web_access_info(self):
        # if open=1,returns a list parameter with all allowed macaddresses
        return self.get_api_endpoint("misystem/misystem/web_access_info")

    def set_lan_dhcp(self, dhcp_start=None, dhcp_end=None, disable_dhcp=0, lease_time="720m"):
        # disabble_dhcp on/off:1/0,others are the start and end of dhcp range.192.168.X.start-stop
        if disable_dhcp:
            endpoint_url = f"xqnetwork/set_lan_dhcp?ignore={disable_dhcp}"
        else:
            endpoint_url = f"xqnetwork/set_lan_dhcp?leasetime={lease_time}&start={dhcp_start}&end={dhcp_end}&ignore={disable_dhcp}"
        return self.get_api_endpoint(endpoint_url)

    def set_lan_ip(self, ip):
        # in form of 192.168.X.X
        # sets router ip/DHCP gateway
        return self.get_api_endpoint(f"xqnetwork/set_lan_ip?ip={ip}")

    def set_sys_time(self, time=None, timezone=None):
        # set system timezone or time.one should exist at same time
        # timezone=%3C%2B0330%3E-3%3A30%3C%2B0430%3E%2CJ79%2F24%2CJ263%2F24
        # <+0330>-3:30<+0430>,J79/24,J263/24
        # TODO:parameters?

        # OR for time :
        # time=2021-9-7+15%3A32%3A56
        # time=2021-9-7 15:32:56
        data = {
            "timezone": timezone,
            "time": time,
        }
        if timezone:
            raise NotImplementedError
        return self.post_api_endpoint("misystem/set_sys_time", data=data)

    def qos_switch(self, on):
        # on : qos on/off:1/0
        return self.get_api_endpoint(f"misystem/qos_switch?on={on}")

    def qos_mode(self, mode):
        # TODO:modes?
        return self.get_api_endpoint(f"misystem/qos_mode?mode={mode}")

    def qos_limits(self, data):
        # put limit for each macaddress:
        # data array of dicts.every dict has "mac","maxup","maxdown" in kilobytes/s
        return self.post_api_endpoint("misystem/qos_limits", data=data)

    def mac_bind(self, data):
        # static ip for DHCP
        # data array of dicts,every dict has "ip","mac","name"
        return self.post_api_endpoint("xqnetwork/mac_bind", data=data)

    def macunbind(self, mac):
        # remove static ip for DHCP
        data = {"mac": mac}
        return self.post_api_endpoint("xqnetwork/mac_unbind", data=data)

    def add_server(self, username, password, domain, enable, ddns_id):
        # add DDNS server.
        # TODO:Check different providers parameters:
        return self.get_api_endpoint(
            f"xqnetwork/add_server??username={username}&password={password}&checkinterval=8569&forceinterval=6985&domain={domain}&enable={enable}&id={ddns_id}")

    def server_switch(self, ddns_id, on):
        # turn on ddns id on/off
        return self.get_api_endpoint(f"xqnetwork/server_switch?id={ddns_id}&on={on}")

    def del_server(self, ddns_id):
        # delete ddns entry
        return self.get_api_endpoint(f"xqnetwork/del_server?id={ddns_id}")

    def add_redirect(self, name, proto, outer_port, ip, internal_port):
        # add port_forward
        # name=test&proto=1&sport=1234&ip=192.168.31.XXX&dport=4321
        # proto:UDP = 1 | TCP = 2 | UDP And TCP= 3
        # TODO:check udp and tcp parameters to be sure
        data = {"name": name,
                "proto": proto,
                "sport": outer_port,
                "ip": ip,
                "dport": internal_port
                }
        return self.post_api_endpoint("xqnetwork/add_redirect", data=data)

    def delete_redirect(self, port):
        # delete single port forward
        data = {"port": port}
        return self.post_api_endpoint("xqnetwork/delete_redirect", data=data)

    def smartvpn_switch(self, enable, mode):
        # enable 1/0
        # modes: traffic by service:1 | traffic by device:2
        return self.get_api_endpoint(f"misystem/smartvpn_switch?enable={enable}&mode={mode}")

    def smartvpn_mac(self, mac, delete):
        # mac address and if should be deleted or not(1/0)
        data = {
            "macs:": mac,
            "opt": delete
        }
        return self.post_api_endpoint("misystem/smartvpn_mac", data=data)

    def vpn_status(self):
        # TODO:?!?!
        return self.get_api_endpoint("xqsystem/vpn_status")

    def set_vpn(self, name, protocol, server, username, password):
        # TODO:check normal pptp/l2tp vpn settings
        # oname=123123&proto=pptp&server=serverserver&username=useruser&password=passpass
        # protocols:pptp|l2tp
        data = {
            "onname": name,
            "proto": protocol,
            "server": server,
            "username": username,
            "password": password,

        }
        return self.post_api_endpoint("xqsystem/set_vpn", data=data)

    def vpn_switch(self, enable, id):
        # enable/disable vpn
        # should manually enable vpn after adding it
        # id from vpn api
        return self.get_api_endpoint(f"xqsystem/vpn_switch?conn={enable}&id={id}")

    def del_vpn(self, id):
        # delete a vpn using its id
        return self.get_api_endpoint(f"xqsystem/del_vpn?id={id}")

    def upnp_switch(self, enable):
        # turn upnpn on/off(1/0)
        return self.get_api_endpoint(f"xqsystem/upnp_switch?switch={enable}")

    def mi_vpn(self):
        # TODO:?!?!
        raise NotImplementedError
        return "misystem/mi_vpn"

    def set_language(self):
        # TODO ?!?!?!?!
        raise NotImplementedError
        # POST
        return "xqsystem/set_language"

    def set_router_name(self, name, locale='家'):
        # TODO:locale?!
        # return self.get_api_endpoint(f"misystem/set_router_name?name={name}&locale={locale}")
        return self.get_api_endpoint(f"misystem/set_router_name?name={name}")
