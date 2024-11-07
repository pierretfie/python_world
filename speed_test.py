from speedtest import Speedtest

def test_network_speed():
    net = Speedtest()

    #fetch best server
    best_Server =net.get_best_server()

    #print server details
    print(f"Connected to: {best_Server['host']} in {best_Server['name']}, {best_Server['country']}")
    print(f"latency(Ping): {best_Server['latency']}ms")

    #test
    download_speed = net.download()/ 1_000_000 #bits to Mbps
    upload_speed = net.upload()/ 1_000_000 #bits to Mbps
    download_speed = download_speed / 8 #bits to bytes
    upload_speed = upload_speed / 8 #bits to bytes

    #get ping

    ping = net.results.ping
    print(f"Download Speed: {download_speed:.2f} MBps")
    print(f"Upload Speed: {upload_speed:.2f} MBps")
    print(f"Ping: {ping:.2f} ms")

if __name__ == "__main__":
    test_network_speed()
