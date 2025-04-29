#!/usr/bin/env python3

# Copyright (c) 2024 John Doe
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the {copyright_holder} nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import unittest

from ament_index_python.packages import get_package_share_directory

import launch
import launch_ros
import launch_testing
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_test_description():
    diffbot_launch_file = os.path.join(
        get_package_share_directory("ros2_control_demo_example_2"),
        "launch",
        "diffbot.launch.py",
    )

    # Mock hardware to test 4-wheel configuration
    use_mock_hardware = "true"

    diffbot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(diffbot_launch_file),
        launch_arguments={
            "use_mock_hardware": use_mock_hardware,
            "gui": "false",
        }.items(),
    )

    return launch.LaunchDescription(
        [
            diffbot_launch,
            # Start tests right away - no need to wait for anything
            launch_testing.actions.ReadyToTest(),
        ]
    )


class Test4WheelDiffBotLaunchTestCase(unittest.TestCase):
    def test_processes_alive(self, proc_info):
        """Test that the required processes are running."""
        proc_info.assertWaitForStartup(timeout=10.0)

        # Check if the required nodes are running
        proc_output = proc_info.process("controller_manager").get_output()
        self.assertIn("controller_manager", proc_output)


@launch_testing.post_shutdown_test()
class Test4WheelDiffBotLaunchTestCaseAfterShutdown(unittest.TestCase):
    def test_processes_exit_code(self, proc_info):
        """Test that the process exited with code 0."""
        launch_testing.asserts.assertExitCodes(proc_info)


if __name__ == "__main__":
    unittest.main()