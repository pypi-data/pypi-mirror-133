import unittest
import os
from permission_check.permission_check import PermissionCheck
from permission_check.utils import Permission


class TestFileLoading(unittest.TestCase):

    def test_valid_file_load(self):
        self.assertRaises(AssertionError, self.assertRaises, FileNotFoundError, PermissionCheck,
                          os.path.join(os.getcwd(), "setup.py"))

    def test_invalid_file_load(self):
        self.assertRaises(FileNotFoundError, PermissionCheck, "setup1.py")

    def test_valid_folder_load(self):
        self.assertRaises(AssertionError, self.assertRaises, FileNotFoundError, PermissionCheck,
                          os.path.join(os.getcwd(), "permission_check"))

    def test_invalid_folder_load(self):
        self.assertRaises(FileNotFoundError, PermissionCheck, "permission_check1")


class TestFilePermissions(unittest.TestCase):
    file = PermissionCheck(os.path.join(os.getcwd(), "setup.py"))

    def test_valid_file(self):
        self.assertRegex(TestFilePermissions.file.permissions, r"^\d{3}$")

    def test_valid_folder(self):
        folder = PermissionCheck(os.path.join(os.getcwd(), "permission_check"))
        self.assertRegex(folder.permissions, r"^\d{3}$")

    def test_owner_permission(self):
        self.assertIsInstance(TestFilePermissions.file.owner.has_all(), bool)

    def test_group_permission(self):
        self.assertIsInstance(TestFilePermissions.file.group.has_all(), bool)

    def test_others_permission(self):
        self.assertIsInstance(TestFilePermissions.file.others.has_all(), bool)


class TestPermissionUtilityHasAll(unittest.TestCase):
    permission = Permission("7")

    def test_has_all(self):
        self.assertTrue(TestPermissionUtilityHasAll.permission.has_all())

    def test_has_read(self):
        self.assertTrue(TestPermissionUtilityHasAll.permission.has_read())

    def test_has_write(self):
        self.assertTrue(TestPermissionUtilityHasAll.permission.has_write())

    def test_has_execute(self):
        self.assertTrue(TestPermissionUtilityHasAll.permission.has_execute())


class TestPermissionUtilityHasRead(unittest.TestCase):
    permission1 = Permission("4")
    permission2 = Permission("6")
    permission3 = Permission("5")

    def test_has_read1(self):
        self.assertTrue(TestPermissionUtilityHasRead.permission1.has_read())

    def test_has_read2(self):
        self.assertTrue(TestPermissionUtilityHasRead.permission2.has_read())

    def test_has_read3(self):
        self.assertTrue(TestPermissionUtilityHasRead.permission3.has_read())

    def test_has_write(self):
        self.assertFalse(TestPermissionUtilityHasRead.permission3.has_write())

    def test_has_execute(self):
        self.assertFalse(TestPermissionUtilityHasRead.permission2.has_execute())


class TestPermissionUtilityHasWrite(unittest.TestCase):
    permission1 = Permission("2")
    permission2 = Permission("6")
    permission3 = Permission("3")

    def test_has_write1(self):
        self.assertTrue(TestPermissionUtilityHasWrite.permission1.has_write())

    def test_has_write2(self):
        self.assertTrue(TestPermissionUtilityHasWrite.permission2.has_write())

    def test_has_write3(self):
        self.assertTrue(TestPermissionUtilityHasWrite.permission3.has_write())

    def test_has_read(self):
        self.assertFalse(TestPermissionUtilityHasWrite.permission3.has_read())

    def test_has_execute(self):
        self.assertFalse(TestPermissionUtilityHasWrite.permission2.has_execute())


class TestPermissionUtilityHasExecute(unittest.TestCase):
    permission1 = Permission("1")
    permission2 = Permission("5")
    permission3 = Permission("3")

    def test_has_execute1(self):
        self.assertTrue(TestPermissionUtilityHasExecute.permission1.has_execute())

    def test_has_execute2(self):
        self.assertTrue(TestPermissionUtilityHasExecute.permission2.has_execute())

    def test_has_execute3(self):
        self.assertTrue(TestPermissionUtilityHasExecute.permission3.has_execute())

    def test_has_read(self):
        self.assertFalse(TestPermissionUtilityHasExecute.permission3.has_read())

    def test_has_write(self):
        self.assertFalse(TestPermissionUtilityHasExecute.permission2.has_write())


if __name__ == "__main__":
    unittest.main()
