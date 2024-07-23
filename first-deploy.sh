#!/bin/bash

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
