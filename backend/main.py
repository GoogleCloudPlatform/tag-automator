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

"""Tag Automator to easily manage tags from GCP resources."""

import os
from flask import Flask, jsonify, request, Blueprint
from list_possible_tags import getTags
from update_resources_tags import update_gcp_tags, bulk_update_gcp_tags
from list_resources_tags import formatResources, search_resources_by_type
from delete_resources_tags import del_gcp_tags

scope = os.environ.get("SCOPE")

if not scope:
    raise Exception("SCOPE env variable must be provided.")

asset_type = os.environ.get(
    "ASSET_TYPES",
    [
        "compute.googleapis.com/Instance",
        "storage.googleapis.com/Bucket",
        "bigquery.googleapis.com/Table",
        "bigquery.googleapis.com/Dataset",
        "sqladmin.googleapis.com/Instance",
        "cloudresourcemanager.googleapis.com/Folder",
        "cloudresourcemanager.googleapis.com/Organization",
        "cloudresourcemanager.googleapis.com/Project",
        "run.googleapis.com/Service",
        "container.googleapis.com/Cluster",
        "compute.googleapis.com/Network",
        "compute.googleapis.com/Subnetwork",
    ],
)

api = Blueprint("api", __name__, url_prefix="/api")


# Endpoint 2: GET /resources
@api.route("/resources", methods=["GET"])
def get_resources():
    """Retrieve resources based on filters."""
    instance_resources = search_resources_by_type(scope, asset_type)
    filtered_resources = formatResources(instance_resources)
    return jsonify(filtered_resources)


# Endpoint 3: GET /tags
@api.route("/tags", methods=["GET"])
def get_tags():
    """List all available tags."""
    return jsonify(getTags(scope))


# Endpoint 4: POST /resource
@api.route("/resource", methods=["POST"])
def create_resource():
    """Create a new resource."""
    data = request.get_json()

    if not all(key in data for key in ("id", "tags")):
        return jsonify({"error": "Missing required fields (id, tags)"}), 400

    response = update_gcp_tags(data.get("id"), data.get("tags"), data.get("location"))

    if response:
        return (jsonify({"message": "Tag applied created successfully"}), 200)

    return (jsonify({"message": "Fail to apply tags on resource"}), 500)


# Endpoint 4: DEL /resource
@api.route("/resources/tags", methods=["DELETE"])
def delete_tags_from_resources():
    """Delete tags from multiple resources."""
    data = request.get_json()

    response = del_gcp_tags(data.get("resources"), data.get("tags"))

    if not response:
        return (
            jsonify({"message": "Tags delete successfully", "errors": response}),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "message": "Fail to apply tags on resources",
                    "errors": response,
                }
            ),
            200,
        )


# Endpoint : POST /resource/tags
@api.route("/resources/tags", methods=["POST"])
def bulk_tags_from_resources():
    """Add tags to multiple resources."""
    data = request.get_json()

    if not all(key in data for key in ("resources", "tags")):
        return jsonify({"error": "Missing required fields (id, tags)"}), 400

    response = bulk_update_gcp_tags(data.get("resources"), data.get("tags"), scope)

    if not response:
        return (
            jsonify(
                {"message": "Tag applied created successfully", "errors": response}
            ),
            200,
        )
    else:
        return (
            jsonify({"message": "Fail to apply tags on resource", "errors": response}),
            200,
        )


app = Flask(__name__)
app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)
