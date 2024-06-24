import objc
from CoreWLAN import CWWiFiClient
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

def dB_from_quality(quality):
    return float(quality) / 2 - 100

def list_current_wifi():
    try:
        # Create a Wi-Fi client instance
        wifi_client = CWWiFiClient.sharedWiFiClient()
        interface = wifi_client.interface()
        
        # Get the current SSID
        current_ssid = interface.ssid()
        
        if current_ssid:
            bssid = current_ssid
            channel = interface.wlanChannel().channelNumber()
            signal_level = interface.rssiValue()
            quality = percentage_from_db(signal_level)
            
            response = {
                "iface": interface.interfaceName(),
                "ssid": current_ssid,
                "bssid": bssid,
                "mac": bssid,
                "mode": "Unknown",  # CoreWLAN does not provide mode directly
                "channel": channel,
                "frequency": frequency_from_channel(channel),
                "signal_level": signal_level,
                "quality": quality,
                "security": "Unknown",  # CoreWLAN does not provide security directly
                "security_flags": [],  # CoreWLAN does not provide security flags directly
                "success": True
            }
            print(json.dumps(response))
        else:
            print(json.dumps({"error": "No Wi-Fi connection found.", "success": False}))
    
    except Exception as e:
        print(json.dumps({"error": str(e), "success": False}))

if __name__ == "__main__":
    list_current_wifi()
