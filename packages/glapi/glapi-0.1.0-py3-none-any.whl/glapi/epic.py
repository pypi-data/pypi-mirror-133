from glapi import configuration
from glapi.connection import GitlabConnection

class GitlabEpic:
    """
    GitlabEpic is a Gitlab Epic.
    """

    def __init__(self, id: str = None, iid: str = None, epic: dict = None, group_id: str = None, token :str = configuration.GITLAB_TOKEN, version: str = configuration.GITLAB_API_VERSION):
        """
        Args:
            id (string): GitLab Epic id
            iid (string): GitLab Epic iid
            epic (dictionary): GitLab Epic
            group_id (string): Gitlab Group id
            token (string): GitLab personal access, ci, or deploy token
            version (string): GitLab API version as base url
        """
        self.connection = GitlabConnection(
            token=token,
            version=version
        )
        self.epic = epic if epic else (self.connection.query("groups/%s/epics/%s" % (group_id, iid))["data"] if id and token and version else None)
        self.group_id = self.epic["group_id"] if self.epic else None
        self.id = self.epic["id"] if self.epic else None
        self.iid = self.epic["iid"] if self.epic else None

    def extract_notes(self) -> list:
        """
        Extract epic-specific note data (comments).

        Returns:
            A list of dictionaries where each represents a GtiLab Note.
        """

        result = None

        # check connection params
        if self.id and self.connection.token and self.connection.version:

            # query api
            result = self.connection.paginate(
                endpoint="groups/%s/epics/%s/notes" % (
                    self.group_id,
                    self.iid
                )
            )

        return result
