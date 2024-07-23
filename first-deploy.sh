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

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Missing service account and scope - usage: $0 service-account@your-project.iam.gserviceaccount.com organizations/12345678"
  exit 1
fi

SA=$1
SCOPE=$2

echo "Deploying frontend..."
cd frontend
./deploy.sh $SA
cd ..

echo "Deploying backend..."
cd backend
sed "s|{SCOPE}|$SCOPE|g" "backend-template.yaml" > "backend.yaml"
./deploy.sh $SA
cd ..

echo "Setting up dispatch..."
gcloud app deploy dispatch.yaml --project=$(echo "$1" | cut -d '@' -f 2 | cut -d '.' -f 1)

printf "\nDone!\n"
