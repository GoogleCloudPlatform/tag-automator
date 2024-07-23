#!/bin/bash

if [ -z "$1" ]; then
  echo "Missing service account - usage: $0 service-account@your-project.iam.gserviceaccount.com"
  exit 1
fi

PROJECT_ID=$(echo "$1" | cut -d '@' -f 2 | cut -d '.' -f 1)

gcloud app deploy backend.yaml --project=$PROJECT_ID --service-account=$1
