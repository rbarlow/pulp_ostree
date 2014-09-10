from gettext import gettext as _

from pulp.client import parsers
from pulp.client.commands.repo.cudl import CreateAndConfigureRepositoryCommand
from pulp.client.commands.repo.cudl import UpdateRepositoryCommand
from pulp.client.commands.repo.importer_config import ImporterConfigMixin
from pulp.client.extensions.extensions import PulpCliOption
from pulp.common.constants import REPO_NOTE_TYPE_KEY

from pulp_ostree.common import constants

d = _('if "true", on each successful sync the repository will automatically be '
      'published; if "false" content will only be available after manually publishing '
      'the repository; defaults to "true"')

OPT_AUTO_PUBLISH = PulpCliOption(
    '--auto-publish', d, required=False, parse_func=parsers.parse_boolean)


IMPORTER_CONFIGURATION_FLAGS = dict(
    include_ssl=False,
    include_sync=True,
    include_unit_policy=False
)


class CreateOSTreeRepositoryCommand(CreateAndConfigureRepositoryCommand, ImporterConfigMixin):

    IMPORTER_TYPE_ID = constants.WEB_IMPORTER_TYPE_ID

    default_notes = {REPO_NOTE_TYPE_KEY: constants.REPO_NOTE_OSTREE}

    def __init__(self, context):
        CreateAndConfigureRepositoryCommand.__init__(self, context)
        ImporterConfigMixin.__init__(self, **IMPORTER_CONFIGURATION_FLAGS)
        self.add_option(OPT_AUTO_PUBLISH)

    def _describe_distributors(self, user_input):
        """
        Subclasses should override this to provide whatever option parsing
        is needed to create distributor configs.

        :param user_input:  dictionary of data passed in by okaara
        :type  user_input:  dict

        :return:    list of dict containing distributor_type_id,
                    repo_plugin_config, auto_publish, and distributor_id (the same
                    that would be passed to the RepoDistributorAPI.create call).
        :rtype:     list of dict
        """
        auto_publish = user_input.get(OPT_AUTO_PUBLISH.keyword, True)

        distributors = [
            dict(distributor_type_id=constants.WEB_DISTRIBUTOR_TYPE_ID,
                 distributor_config={},
                 auto_publish=auto_publish,
                 distributor_id=constants.WEB_DISTRIBUTOR_TYPE_ID),
        ]

        return distributors


class UpdateOSTreeRepositoryCommand(UpdateRepositoryCommand, ImporterConfigMixin):

    def __init__(self, context):
        UpdateRepositoryCommand.__init__(self, context)
        ImporterConfigMixin.__init__(self, **IMPORTER_CONFIGURATION_FLAGS)
        self.add_option(OPT_AUTO_PUBLISH)

    def run(self, **kwargs):
        web_config = {}

        auto_publish = kwargs.pop(OPT_AUTO_PUBLISH.keyword, None)
        if auto_publish:
            dist_config[constants.AUTO_PUBLISH] = value

        if dist_config:
        kwargs['distributor_configs'][constants.WEB_DISTRIBUTOR_TYPE_ID] = dist_config

        super(UpdateOSTreeRepositoryCommand, self).run(**kwargs)
