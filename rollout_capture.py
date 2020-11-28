from inc.ssh_client import *
from inc.config import *


def sniff_packet(node, port_idx = 0):
    sniffer = (SSHConnector(host=node.host, user=USER, gss_auth=True, gss_kex=True, logfile="log/snifflogger_" + node.node_name))
    # sniffer = SSHConnector(host="192.168.0.3", user=USER, logfile="log/snifflogger_"+ node.node_name+".log")
    sniffer.connect()
    return 1
    # sniffer.open_shell()
    # out = sniffer.execute(
    #     "python "+config.config_data["time_ref_script"]["directory"]+ " -ip " + str(node.ip) + " -p " + str(node.ports[port_idx]),
    #     config.config_data["time_ref_script"]["expected_start"],
    #     config.config_data["time_ref_script"]["failed_out"])
    # time_ref = string_between(out, config.config_data["time_ref_script"]["expected_start"],config.config_data["time_ref_script"]["expected_end"])
    # return time_ref


config = Config("./config", "config.json")
client_list = []

time_ref = sniff_packet(config.numa_list[0])
#
#
# for idx, node in enumerate(config.numa_list):
#     node.cmd_pattern += " -f " + time_ref
#     client_list.append(SSHConnector(host="192.168.0.3", user="niclas", password="cAevN3SC", logfile="log/logger.log"))
#     # client_list.append(SSHConnector(host=node.host, user=USER, logfile="log/logger_" + node.node_name))
#     client_list[idx].connect()
#     client_list[idx].open_shell()
#     client_list[idx].execute("echo '" + node.cmd_pattern + "' >> "+config.config_data["launch_script"]["directory"]+"command_line_args.txt; echo success", "success", "failed")
#     client_list[idx].execute("python "+config.config_data["launch_script"]["directory"]+config.config_data["launch_script"]["name"]+ " -i " +str(node.node_name) + " -d command_line_args",
#         config.config_data["launch_script"]["expected_start"],
#         config.config_data["launch_script"]["failed_out"])
