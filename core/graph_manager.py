import boto3
from graphviz import Digraph

class SGGraph():
    def __init__(self, aws_profile, aws_region, ignore_strs, colors):
        self._sgs = {}
        self._ignore_strs = ignore_strs
        self._colors = colors

        # aws
        _aws_session = boto3.Session(profile_name=aws_profile)
        self._ec2client = _aws_session.client('ec2', region_name=aws_region)
        self._aws_region = aws_region

    def _sg_ignore(self, sg_name):
        for ignore_str in self._ignore_strs:
            if ignore_str in sg_name:
                return True
        return False

    def _get_sgs(self):
        sgs = self._ec2client.describe_security_groups()
        sgs = sgs["SecurityGroups"]
        for sg in sgs:
            self._get_sg(sg)

    def _get_sg(self, sg):
        sg_name = sg["GroupName"]
        if not self._sg_ignore(sg_name):
            sg_id = sg["GroupId"]
            self._sgs[sg_id] = {
                "name": sg["GroupName"],
                "ports": {}
            }
            ports = sg["IpPermissions"]
            for port in ports:
                self._get_port(sg, port)

    def _get_port(self, sg, port):
        if "FromPort" in port:
            if port["FromPort"] != port["ToPort"]:
                port_range = "{}-{}".format(port["FromPort"], port["ToPort"])
            else:
                port_range = port["FromPort"]

            sg_id = sg["GroupId"]
            self._sgs[sg_id]["ports"][port_range] = {
                "protocol": port["IpProtocol"],
                "sgs": [sg["GroupId"] for sg in port["UserIdGroupPairs"]],
                "ips": [ip["CidrIp"] for ip in port["IpRanges"]],
            }

    def _colorize(self, proto, port_id):
        label = "{}:{}".format(proto, port_id)
        port = str(port_id)
        color = self._colors.get(port, "black")
        label = '<<font color="{}">{}</font>>'.format(color, label)
        return label, color

    def sgs_2_graph(self):
        self._get_sgs()

        graph = Digraph(comment=self._aws_region)
        graph.attr(nodesep="1")
        graph.attr(ranksep="4")

        for sg_id, sg_info in self._sgs.items():
            name = sg_info["name"]
            # Set links
            for port_id, port_info in sg_info["ports"].items():
                for sg in port_info["sgs"]:
                    proto = port_info["protocol"]
                    label, color = self._colorize(proto, port_id)
                    graph.edge(sg, sg_id, label=label, color=color)
                for ip in port_info["ips"]:
                    name = "{}\n[{}]:{}".format(name, ip, port_id)
            # Create item (SG)
            graph.node(sg_id, name)
        graph.view(self._aws_region + ".graph")
