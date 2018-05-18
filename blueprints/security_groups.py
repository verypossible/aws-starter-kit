from stacker.blueprints.base import Blueprint

from troposphere import (
        Output,
        Ref,
)
from troposphere import ec2


class SecurityGroupRules(Blueprint):

    BASTION_SG_NAME = 'BastionSecurityGroup'
    CLIENT_SG_NAME = 'ClientSeverlessSecurityGroup'
    RDS_SG_NAME = 'RDSSecurityGroup'
    VERY_SG_NAME = 'VeryTeamSecurityGroup'

    VARIABLES = {
        "VpcId": {
            "type": str,
            "description": "VpcId",
        },
        "BastionSecurityGroup": {
            "type": str,
            "description": "Security group for the bastion host",
            "default": "",
        },
        "BastionIPWhitelist": {
            "type": list,
            "description": "List of IP addresses to allow port 22 to Bastion host",
            "default": [],
        },

    }

    def _create_sg(self, name, description):
        t = self.template
        variables = self.get_variables()
        sg = t.add_resource(
            ec2.SecurityGroup(
                name,
                VpcId=variables['VpcId'],
                GroupDescription=description,
            )
        )
        t.add_output(Output("%sId" % name, Value=Ref(sg)))

    def create_serverless_sg(self):
        """Create a security group for client Serverless functions"""
        self._create_sg(self.CLIENT_SG_NAME, 'Security group for Serverless functions')

    def create_rds_sg(self):
        """Create a security group for RDS"""
        self._create_sg(self.RDS_SG_NAME, 'Security group for Client RDS')

    def create_veryteam_sg(self):
        """Create a security group for RDS"""
        self._create_sg(self.VERY_SG_NAME, 'Security group for Very Team')

    def create_whitelist_rules(self):
        variables = self.get_variables()
        ips = variables.get('BastionIPWhitelist')
        if not ips:
            return

        bastion_sg = variables['BastionSecurityGroup']
        for i, ip in enumerate(ips):
            self.template.add_resource(
                ec2.SecurityGroupIngress(
                    'WhiteListIPAllPorts%s' % i,
                    IpProtocol="tcp",
                    FromPort="22",
                    ToPort="22",
                    CidrIp="%s/32" % (ip, ),
                    GroupId=bastion_sg,
                )
            )

    def create_db_rules(self):
        self.template.add_resource(
            ec2.SecurityGroupIngress(
                'ClientPsqlPort5432',
                IpProtocol="tcp",
                FromPort="5432",
                ToPort="5432",
                SourceSecurityGroupId=Ref(self.CLIENT_SG_NAME),
                GroupId=Ref(self.RDS_SG_NAME),
            )
        )

        # If there is a bastion sg, add inbound access from the bastion to RDS.
        variables = self.get_variables()
        bastion_sg = variables[self.BASTION_SG_NAME]
        if bastion_sg:
            self.template.add_resource(
                ec2.SecurityGroupIngress(
                    'BastionPsqlPort5432',
                    IpProtocol="tcp",
                    FromPort="5432",
                    ToPort="5432",
                    SourceSecurityGroupId=bastion_sg,
                    GroupId=Ref(self.RDS_SG_NAME),
                )
            )

    def create_template(self):
        self.create_serverless_sg()
        self.create_rds_sg()
        self.create_db_rules()
        self.create_veryteam_sg()
        self.create_whitelist_rules()
