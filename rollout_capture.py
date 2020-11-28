from inc.ssh_client import *
from inc.config import *


def sniff_packet(node, port_idx = 0):
    print("Sniffing packet on "+node.host+":"+str(node.ports[port_idx])+"to determine time reference")
    sniffer = (SSHConnector(host=node.host, user=USER, gss_auth=True, gss_kex=True, logfile="log/snifflogger_" + node.node_name))
    # sniffer = SSHConnector(host="192.168.0.3", user=USER, logfile="log/snifflogger_"+ node.node_name+".log")
    sniffer.connect()
    sniffer.open_shell()
    out = sniffer.execute(
        "python "+config.config_data["script_dir"]+config.config_data["time_ref_script"]["name"]+ " -i " + str(node.ip) + " -p " + str(node.ports[port_idx]),
        config.config_data["time_ref_script"]["expected_start"],
        config.config_data["time_ref_script"]["failed"])
    sniffer.close()
    time_ref = string_between(out, config.config_data["time_ref_script"]["expected_start"],config.config_data["time_ref_script"]["expected_end"])
    print("Time reference is: "+time_ref)
    return time_ref


config = Config("./config", "config.json")
script_dir = config.config_data["script_dir"]
time_ref = sniff_packet(config.numa_list[0])

# Create a server to communicate with launch_capture programs
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(ip, port)
sock.listen(config.numa_list.size())
conn, addr = sock.accept()

client_list = []


print("Launching capture dockers on pacifix nodes")

for idx, node in enumerate(config.numa_list):
    node.cmd_pattern += " -f " + time_ref
    node.ssh_client = SSHConnector(host=node.host, user=USER, gss_auth=True, gss_kex=True, logfile="log/logger_" + node.node_name)
    node.ssh_client.connect()
    node.ssh_client.open_sftp()
    node.ssh_client.upload("config/header_dada.txt", config.config_data["dir_to_dada_header_file"])
    node.ssh_client.open_shell()
    node.ssh_client.execute("echo '"+node.cmd_pattern+"' >> "+script_dir+"command_line_args.txt; echo success", "success", "fail")
    launch_cmd = "python "+script_dir+config.config_data["launch_script"]["name"]+ " -n " +str(node.node_name) + " -c "+script_dir+"command_line_args.txt"
    print(launch_cmd)
    out = node.ssh_client.execute(launch_cmd,
        config.config_data["launch_script"]["expected_start"],
        config.config_data["launch_script"]["failed"])


stop = raw_input("Enter key to stop capture...")

for node in config.numa_list:
    shutdown_cmd = "python " + script_dir + config.config_data["shutdown_script"]["name"] + " -n " + node.node_name
    node.ssh_client.execute(shutdown_cmd,
        config.config_data["shutdown_script"]["expected_start"],
        config.config_data["shutdown_script"]["failed"])
    print("Docker stopped on " +  node.node_name)

sleep(2)

for node in config.numa_list:
    node.ssh_client.close()
