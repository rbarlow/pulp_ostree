from gettext import gettext as _

from pulp.client.commands.repo import cudl
from pulp.client.extensions.decorator import priority

from pulp_ostree.extensions.admin.cudl import CreateOSTreeRepositoryCommand
from pulp_ostree.extensions.admin.cudl import UpdateOSTreeRepositoryCommand


SECTION_ROOT = 'ostree'
DESC_ROOT = _('manage ostree repositories')

SECTION_REPO = 'repo'
DESC_REPO = _('repository lifecycle commands')


@priority()
def initialize(context):
    """
    create the docker CLI section and add it to the root

    :type  context: pulp.client.extensions.core.ClientContext
    """
    root_section = context.cli.create_section(SECTION_ROOT, DESC_ROOT)
    add_repo_section(context, root_section)


def add_repo_section(context, parent_section):
    """
    add a repo section to the docker section

    :type  context: pulp.client.extensions.core.ClientContext
    :param parent_section:  section of the CLI to which the repo section
                            should be added
    :type  parent_section:  pulp.client.extensions.extensions.PulpCliSection
    """
    section = parent_section.create_subsection(SECTION_REPO, DESC_REPO)
    section.add_command(CreateOSTreeRepositoryCommand(context))
    section.add_command(cudl.DeleteRepositoryCommand(context))
    section.add_command(UpdateOSTreeRepositoryCommand(context))
    return section
