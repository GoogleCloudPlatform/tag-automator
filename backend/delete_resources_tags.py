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
