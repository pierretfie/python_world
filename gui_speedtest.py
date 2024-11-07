import tkinter as tk
from speedtest import Speedtest

def test_network_speed():

    #change button text
    start_button.config(text="Running....", state=tk.DISABLED)
    result_label.config(text="please wait.......", fg='blue')
    net = Speedtest()

    #fetch best server
    best_Server =net.get_best_server()

    #print server details
   

    #test
    download_speed = net.download()/ 1_000_000 #bits to Mbps
    upload_speed = net.upload()/ 1_000_000 #bits to Mbps
    download_speed = download_speed / 8 #bits to bytes
    upload_speed = upload_speed / 8 #bits to bytes

    #get ping

    ping = net.results.ping
    result_text = (
        f'Download Speed: {download_speed:.2f} MBps\n'
        f'Upload Speed: {upload_speed:.2f} MBps\n'
        f'Latency: {ping:.2f} ms\n'
    )
    result_label.config(text=result_text)

    start_button.config(text="Start Test", state=tk.NORMAL)

#set GUI window
window = tk.Tk()
window.title("Network Speed Test")
#set window size
window.geometry("400x200")
window.resizable(False, False)


#window for display
result_label = tk.Label(window, text="Click start to begin Network Speed Test", wraplength=400, font=("Helvetica", 14), padx=10, pady=10)
result_label.pack()

#button to trigger test
start_button = tk.Button(window, text="Start Test", command=test_network_speed, font=("Helvetica", 12), bg="blue", fg="white", padx=10, pady=5)
start_button.pack()


#run GUI
window.mainloop()
