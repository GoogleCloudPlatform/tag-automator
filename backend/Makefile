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


# Makefile for Flask API Testing

# Set the API base URL (adjust if running on a different port or host)
API_BASE_URL := http://127.0.0.1:5000

# Test Targets

test-all: test-refresh test-get-resources test-get-tags test-post-resource

test-refresh:
	curl $(API_BASE_URL)/api/refresh

test-get-resources:
	curl $(API_BASE_URL)/api/resources

#	curl $(API_BASE_URL)/resources?type=VM
#	curl $(API_BASE_URL)/resources?name=instance-20240618-185825
#	curl $(API_BASE_URL)/resources?tag_key=tag-automator/BU

test-get-tags:
	curl $(API_BASE_URL)/api/tags

test-post-resource:
	curl -X POST -H "Content-Type: application/json" -d '{"id": "//compute.googleapis.com/projects/tag-automator-app/zones/southamerica-east1-b/instances/7732211548561519133",  "tags": [{"key": "tagKeys/281484915300179", "value": "tagValues/281483182417574"}]}' $(API_BASE_URL)/api/resource
