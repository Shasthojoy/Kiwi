# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2018 the Kiwi TCMS project. All rights reserved.
#   Author: Alexander Todorov <info@kiwitcms.org>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from tcms_api.immutable import Status
from tcms_api.mutable import CaseRun

from tcms_api.tests import BaseAPIClient_TestCase

from tcms.testruns.models import TestCaseRunStatus


class TestCaseRunTests(BaseAPIClient_TestCase):
    def test_updating_status_works_as_expected(self):
        """
            Check that after updating TestCaseRun status via the API the
            result in the database actually matches. See
            https://github.com/kiwitcms/Kiwi/issues/184
        """
        # Detach bug and check
        test_case_run = CaseRun(self.caserun.pk)

        for status in TestCaseRunStatus.objects.all():
            test_case_run.status = Status(status.name)
            test_case_run.update()
            self.caserun.refresh_from_db()
            self.assertEqual(self.caserun.case_run_status.name, status.name)
