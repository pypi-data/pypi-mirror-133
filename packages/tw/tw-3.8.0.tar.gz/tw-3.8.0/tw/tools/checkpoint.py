# Copyright 2020 The KaiJIN Authors. All Rights Reserved.
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
# ==============================================================================
import argparse

if __name__ == "__main__":
  # parser
  parser = argparse.ArgumentParser()
  parser.add_argument('--task', type=str, choices=['replace_prefix'])
  parser.add_argument('--src', type=str, default=None)
  parser.add_argument('--dst', type=str, default=None)
  args, _ = parser.parse_known_args()
