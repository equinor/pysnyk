from typing import Any, List, Dict, Optional

import requests

from .models import Organization
from .errors import SnykError


class SnykClient(object):
    API_URL = "https://snyk.io/api/v1/"

    def __init__(self, token: str, url: Optional[str] = None):
        self.api_token = token
        self.api_url = url or self.API_URL
        self.api_headers = {"Authorization": "token %s" % self.api_token}
        self.api_post_headers = self.api_headers
        self.api_post_headers["Content-Type"] = "application/json"

    def _post(self, path: str, obj_json_post_body: Any) -> requests.Response:
        url = "%s/%s" % (self.api_url, path)
        resp = requests.post(
            url, json=obj_json_post_body, headers=self.api_post_headers
        )
        if resp.status_code != requests.codes.ok:
            raise SnykError(resp.json())
        return resp

    def _put(self, path: str, obj_json_post_body: Any) -> requests.Response:
        url = "%s/%s" % (self.api_url, path)
        resp = requests.put(url, json=obj_json_post_body, headers=self.api_post_headers)
        if resp.status_code != requests.codes.ok:
            raise SnykError(resp.json())
        return resp

    def _get(self, path: str) -> requests.Response:
        url = "%s/%s" % (self.api_url, path)
        resp = requests.get(url, headers=self.api_headers)
        if resp.status_code != requests.codes.ok:
            raise SnykError(resp.json())
        return resp

    def _delete(self, path: str) -> requests.Response:
        url = "%s/%s" % (self.api_url, path)
        resp = requests.delete(url, headers=self.api_headers)
        if resp.status_code != requests.codes.ok:
            raise SnykError(resp.json())
        return resp

    # https://snyk.docs.apiary.io/#reference/0/list-members-in-a-group/list-all-members-in-a-group
    def groups_members(self, group_id: str) -> Any:
        path = "org/%s/members" % group_id
        resp = self._get(path)
        obj_json_response_content = resp.json()
        return obj_json_response_content

    @property
    def organizations(self) -> List[Organization]:
        resp = self._get("orgs")
        orgs = []
        if "orgs" in resp.json():
            for org_data in resp.json()["orgs"]:
                orgs.append(Organization.from_dict(org_data))
        for org in orgs:
            org.client = self
        return orgs
