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

"""Module to handle resources tag binding deletes."""

from google.cloud import resourcemanager_v3
from google.api_core.client_options import ClientOptions


def del_gcp_tags(resources, del_tags):
    """Update the tags on a GCP resource."""
    error_list = []
    tag_values = {new_binding["value"] for new_binding in del_tags}

    for resource in resources:
        id = resource.get("id")
        location = resource.get("location")

        endpoint = "cloudresourcemanager.googleapis.com"
        if location is not None and location != "global":
            endpoint = location + "-" + endpoint

        client = resourcemanager_v3.TagBindingsClient(
            client_options=ClientOptions(api_endpoint=endpoint)
        )

        # Retrieve existing tag bindings (handling NotFound for missing resources)
        try:
            current_bindings = client.list_tag_bindings(parent=id)

            tag_bindings_to_remove = []
            for binding in current_bindings:
                if binding.tag_value in tag_values:
                    tag_bindings_to_remove.append(binding)

            for tag_binding in tag_bindings_to_remove:
                client.delete_tag_binding(name=tag_binding.name)

        except Exception as e:
            print(f"Fail to delete tags: {e}")
            error_list.append(id)

    return error_list
