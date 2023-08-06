import datetime

from treelib import Node, Tree

from gitrics import configuration

from glapi.group import GitlabGroup
from glapi.epic import GitlabEpic

class gitricsGroupEpics(GitlabGroup):
    """
    gitricsGroupEpics is a collection of Gitlab Group Epics modified and enriched for gitrics ecosystem.
    """

    def __init__(self, group_id: str = None, group: dict = None, epics: list = None, date_start: str = None, date_end: str = None, token: str = configuration.GITLAB_TOKEN, version: str = configuration.GITLAB_API_VERSION):
        """
        Args:
            date_end (string): iso 8601 date value
            date_start (string): iso 8601 date value
            epics (list): dictionaries of GitLab Epic
            group (dictionary): key/value pair representing a GitLab Group
            group_id (string): GitLab Group id
            token (string): GitLab personal access, ci, or deploy token
            version (string): GitLab API version as base url
        """

        # initialize inheritance
        super(gitricsGroupEpics, self).__init__(
            group=group,
            id=group_id,
            token=token,
            version=version
        )

        # get epics
        self.epics = [GitlabEpic(epic=d) for d in epics] if epics else self.extract_epics(
            date_end=date_end,
            date_start=date_start
        )

        # get notes
        for e in self.epics:
            e.notes = e.extract_notes()

        # build tree
        self.nested = self.nest(self.epics) if self.epics else None

    def nest(self, epics: list, index: int = 0) -> dict:
        """
        Nest epics by parent/child relationship.

        Args:
            epics: (list): GitlabEpic classes where each represents a GitLab Epic

        Returns:
            A generator representing a nested dictionary of parent/child relationships.
        """

        result = Tree()
        tracked = list()
        root = "epics"

        # generate maps to nodes/parents
        nodemap = { d.epic["id"]: d for d in epics }
        parentmap = { d.epic["id"]: d.epic["parent_id"] for d in epics }

        # generate root
        result.create_node(root, root)

        # loop through epics
        for epic in epics:

            nid = epic.id
            pid = epic.epic["parent_id"]

            # has parent
            if pid:

                # parent on tree
                if result.get_node(pid):

                    # node not on tree
                    if result.get_node(nid) is None:

                        # add node to tree
                        result.create_node(nid, nid, parent=pid, data=epic.epic)

                # parent not on tree
                else:

                    # add parent at root
                    result.create_node(pid, pid, parent=root, data=nodemap[pid].epic)

                    # track what was added so later we can update the parent
                    if parentmap[pid]: tracked.append(pid)

                    # add node to tree
                    result.create_node(nid, nid, parent=pid, data=epic.epic)

            # parent is root
            else:

                # node is not on tree
                if result.get_node(nid) is None:

                    # add node to tree
                    result.create_node(nid, nid, parent=root, data=epic.epic)

        # loop through tracked ids
        for id in tracked:

            # move node to proper parent
            result.move_node(id, nodemap[id].epic["parent_id"])

        return result

    def prune(self, epics: list) -> list:
        """
        Prune to epics only with date start or end value.

        Args:
            epics (list): dictionaries where each is a GitLab Epic

        Returns:
            A list of dictionaries where each represents a GitLab Epic.
        """

        return [d for d in epics if d["start_date"] or d["end_date"]] if epics else None
