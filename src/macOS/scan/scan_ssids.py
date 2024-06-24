import objc
from CoreWLAN import CWInterface, CWWiFiClient
import json

def frequency_from_channel(channel):
    channels = {
        **{i: 2412 + 5 * (i - 1) for i in range(1, 15)},
        **{i: 5180 + 10 * (i - 36) for i in range(36, 65, 2)},
        **{i: 5500 + 10 * (i - 100) for i in range(100, 145, 2)},
        **{i: 5745 + 10 * (i - 149) for i in range(149, 162, 2)},
        165: 5825,
        169: 5845,
        173: 5865
    }
    return channels.get(int(channel), None)

def percentage_from_db(db):
    return 2 * (float(db) + 100)

def parse_security(network):
    security_types = {
        0: "None",
        1: "WEP",
        2: "WPA Personal",
        3: "WPA/WPA2 Personal",
        4: "WPA2 Personal",
        5: "Dynamic WEP",
        6: "WPA Enterprise",
        7: "WPA/WPA2 Enterprise",
        8: "WPA2 Enterprise",
        9: "Unknown"
    }

    security = network.securityType()
    return {
        "security": security_types.get(security, "Unknown"),
        "security_flags": []  # Add more detailed flags if needed
    }

def scan_ssid():
    try:
        # Create a Wi-Fi client instance
        wifi_client = CWWiFiClient.sharedWiFiClient()
        interface = wifi_client.interface()
        
        # Scan for networks
        networks, error = interface.scanForNetworksWithName_error_(None, None)
        
        if error:
            return json.dumps({"error": str(error), "success": False})
        
        # Extract details from the networks
        result = []
        for network in networks:
            ssid = network.ssid()
            bssid = interface.bssid() if ssid else None
            channel = network.wlanChannel().channelNumber()
            rssi = network.rssiValue()
            
            network_info = {
                "mac": bssid,
                "bssid": ssid.strip(),
                "ssid": ssid.strip(),
                "channel": channel,
                "frequency": frequency_from_channel(channel),
                "signal_level": rssi,
                "quality": percentage_from_db(rssi),
                **parse_security(network)
            }
            result.append(network_info)
        
        return json.dumps({"networks": result, "success": True})
    
    except Exception as e:
        return json.dumps({"error": str(e), "success": False})

if __name__ == "__main__":
    print(scan_ssid())
