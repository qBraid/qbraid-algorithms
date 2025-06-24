# Copyright 2025 qBraid
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Script for getting/bumping the next pre-release version.

"""

import pathlib

from qbraid_core.system.versions import get_prelease_version

if __name__ == "__main__":
    PACKAGE = "qbraid_algorithms"
    root = pathlib.Path(__file__).parent.parent.resolve()
    version = get_prelease_version(root, PACKAGE)
    print(version)
