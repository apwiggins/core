"""
client.py: implementation of the VnodeClient class for issuing commands
over a control channel to the vnoded process running in a network namespace.
The control channel can be accessed via calls using the vcmd shell.
"""

from core import utils
from core.constants import VCMD_BIN


class VnodeClient:
    """
    Provides client functionality for interacting with a virtual node.
    """

    def __init__(self, name, ctrlchnlname):
        """
        Create a VnodeClient instance.

        :param str name: name for client
        :param str ctrlchnlname: control channel name
        """
        self.name = name
        self.ctrlchnlname = ctrlchnlname

    def _verify_connection(self):
        """
        Checks that the vcmd client is properly connected.

        :return: nothing
        :raises IOError: when not connected
        """
        if not self.connected():
            raise IOError("vcmd not connected")

    def connected(self):
        """
        Check if node is connected or not.

        :return: True if connected, False otherwise
        :rtype: bool
        """
        return True

    def close(self):
        """
        Close the client connection.

        :return: nothing
        """
        pass

    def create_cmd(self, args):
        return f"{VCMD_BIN} -c {self.ctrlchnlname} -- {args}"

    def check_cmd(self, args, wait=True, shell=False):
        """
        Run command and return exit status and combined stdout and stderr.

        :param str args: command to run
        :param bool wait: True to wait for command status, False otherwise
        :param bool shell: True to use shell, False otherwise
        :return: combined stdout and stderr
        :rtype: str
        :raises core.CoreCommandError: when there is a non-zero exit status
        """
        self._verify_connection()
        args = self.create_cmd(args)
        return utils.cmd(args, wait=wait, shell=shell)
