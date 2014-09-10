
import unittest

from mock import patch, Mock
from pulp.common.constants import REPO_NOTE_TYPE_KEY

from pulp_ostree.common import constants
from pulp_ostree.extensions.admin.cudl import (
    OPT_AUTO_PUBLISH, CreateOSTreeRepositoryCommand, UpdateOSTreeRepositoryCommand)


class TestCreateOSTreeRepositoryCommand(unittest.TestCase):

    def test_default_notes(self):
        self.assertEqual(
            CreateOSTreeRepositoryCommand.default_notes.get(REPO_NOTE_TYPE_KEY),
            constants.REPO_NOTE_OSTREE)

    def test_importer_id(self):
        self.assertEqual(
            CreateOSTreeRepositoryCommand.IMPORTER_TYPE_ID,
            constants.WEB_IMPORTER_TYPE_ID)

    def test_describe_distributors(self):
        command = CreateOSTreeRepositoryCommand(Mock())

        # default: True
        user_input = {}
        result = command._describe_distributors(user_input)
        self.assertTrue(result[0][constants.AUTO_PUBLISH])

        # explicit:False
        user_input = {
            OPT_AUTO_PUBLISH.keyword: False
        }
        result = command._describe_distributors(user_input)
        self.assertFalse(result[0][constants.AUTO_PUBLISH])

        # explicit:True
        user_input = {
            OPT_AUTO_PUBLISH.keyword: True
        }
        result = command._describe_distributors(user_input)
        self.assertTrue(result[0][constants.AUTO_PUBLISH])


class TestUpdateOSTreeRepositoryCommand(unittest.TestCase):

    def test_update(self):
        repo_id = 'test'
        user_input = {
            'repo-id': repo_id,
            OPT_AUTO_PUBLISH.keyword: False,
        }

        context = Mock()
        context.config = dict(output=dict(poll_frequency_in_seconds=10))
        context.server.repo.repository.return_value = Mock(response_body={})
        command = UpdateOSTreeRepositoryCommand(context)
        command.run(**user_input)

        delta = {}
        dist_config = {
            constants.WEB_DISTRIBUTOR_TYPE_ID: {
                constants.AUTO_PUBLISH: False
            }
        }

        context.server.repo.update.assert_called_once_with(repo_id, {}, None, dist_config)
