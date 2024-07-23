#!/bin/bash

# Copyright 2024 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

if [ -z "$1" ]; then
  echo "Missing service account - usage: $0 service-account@your-project.iam.gserviceaccount.com"
  exit 1
fi

PROJECT_ID=$(echo "$1" | cut -d '@' -f 2 | cut -d '.' -f 1)

ng build
gcloud app deploy --project=$PROJECT_ID --service-account=$1
