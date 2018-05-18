from stacker_blueprints.rds.postgres import MasterInstance


class PostgresMaster(MasterInstance):
    """Master Postgres RDS which can be made publicly accessiable."""

    def defined_variables(self):
        variables = super(MasterInstance, self).defined_variables()
        variables['PubliclyAccessible'] = {
                "type": bool,
                "description": "Set to 'false' to make the DB private",
                "default": True,
        }

        # allow EngineMajorVersion to be optional by giving it a default value
        variables['EngineMajorVersion']['default'] = ''
        return variables

    def get_common_attrs(self):
        variables = self.get_variables()

        attrs = super(MasterInstance, self).get_common_attrs()
        attrs['PubliclyAccessible'] = variables['PubliclyAccessible']

        # This is to work around a small bug with the default stacker blueprint for RDS.
        # The deletion of a stack will fail when a custom option group is created..this looks like
        # an error CloudFormation itself, for some reason.
        #
        # This blueprint will create a custom option group wwhen EngineMajorVersion is defined.
        # RDS instances have default a default Option Group which will be used if one isn't
        # specified, so this is really an optional parameter.
        #
        # In order to get stack deletion to work:
        #   - Make EngineMajorVersion an optional parameter (in defined_variables)
        #   - Remove the Ref(OptionGroupName) when EngineMajorVersion is blank
        if not variables.get('EngineMajorVersion'):
            attrs.pop('OptionGroupName', None)

        return attrs
