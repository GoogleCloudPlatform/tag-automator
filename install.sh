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

PROJECT_ID=$(gcloud config get project)
read -p "Which project (ID) to install into? (leave blank for \"$PROJECT_ID\"): " NEW_PROJECT_ID
PROJECT_ID=${NEW_PROJECT_ID:-$PROJECT_ID}

REGION="us-east1"
read -p "Which region to use? (leave blank for \"$REGION\"): " NEW_REGION
REGION=${NEW_REGION:-$REGION}

# Create service account
SA_NAME=tag-automator
gcloud iam service-accounts create $SA_NAME --display-name="Tag Automator Backend" --project=$PROJECT_ID

# Creates app for the first time
gcloud app create --region=$REGION --project=$PROJECT_ID

# Enable needed services
gcloud services enable cloudasset.googleapis.com --project=$PROJECT_ID
gcloud services enable cloudresourcemanager.googleapis.com --project=$PROJECT_ID
gcloud services enable iap.googleapis.com --project=$PROJECT_ID

printf "\n\033[0;31mActions:\033[0m\n\n"
printf "\033[0;32m"
printf "==> Go to https://console.cloud.google.com/security/iap?project=$PROJECT_ID and configure your OAuth consent screen!\n\033[0m"
printf "\nAfter that, press enter to continue to deploy\n"
read

gcloud iap web enable --resource-type=app-engine --project=$PROJECT_ID

MEMBERS="user:"$(gcloud auth list --format="value(account)")
read -p "Which user/group/domain to allow access on IAP? (leave blank for \"$MEMBERS): " NEW_MEMBERS
MEMBERS=${NEW_MEMBERS:-$MEMBERS}

# Grant access to members
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member $MEMBERS \
  --role roles/iap.httpsResourceAccessor

read -p "Which scope for tag automator to look for tags/resources? (type projects, folders or organizations) " SCOPE_TYPE
read -p "What's the ID/NUMBER of the resource? " SCOPE_ID

APP_SA="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"
ROLES=("roles/cloudasset.viewer" "roles/resourcemanager.tagUser")

for role in "${ROLES[@]}"; do
  gcloud $SCOPE_TYPE add-iam-policy-binding $SCOPE_ID \
    --member="serviceAccount:"$APP_SA \
    --role="$role"
done

./first-deploy.sh $APP_SA $SCOPE_TYPE/$SCOPE_ID
