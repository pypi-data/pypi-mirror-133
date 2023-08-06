import datetime

import networkx as nx

from gitrics import configuration

from glapi.group import GitlabGroup
from glapi.issue import GitlabIssue

class gitricsGroupIssues(GitlabGroup):
    """
    gitricsGroupIssues is a collection of Gitlab Group Issues modified and enriched for gitrics ecosystem.
    """

    def __init__(self, group_id: str = None, group: dict = None, issues: list = None, date_start: str = None, date_end: str = None, token: str = configuration.GITLAB_TOKEN, version: str = configuration.GITLAB_API_VERSION):
        """
        Args:
            date_end (string): iso 8601 date value
            date_start (string): iso 8601 date value
            issues (list): dictionaries of GitLab Issue
            group (dictionary): key/value pair representing a GitLab Group
            group_id (string): GitLab Group id
            token (string): GitLab personal access, ci, or deploy token
            version (string): GitLab API version as base url
        """

        # initialize inheritance
        super(gitricsGroupIssues, self).__init__(
            group=group,
            id=group_id,
            token=token,
            version=version
        )

        # get issues
        items = [GitlabIssue(issue=d) for d in issues] if issues else self.extract_issues(
            date_end=date_end,
            date_start=date_start
        )

        # get notes
        for i in items:
            i.notes = i.extract_notes()

        # enrich
        self.issues = self.enrich(items)

        # build network
        self.nested = self.nest(self.issues) if self.issues else None

    def enrich(self, issues: list) -> list:
        """
        Enrich with data for gitrics ecosystem.

        Args:
            issues (list): GitlabIssue classes where each represents a GitLab Issue

        Returns:
            A list of dictionaries where each represents an enriched GitLab Issue.
        """

        if issues:

            # loop through issues
            for issue in issues:

                # get links
                links = self.connection.query(
                    endpoint="projects/%s/issues/%s/links" % (
                        issue.issue["project_id"],
                        issue.issue["iid"]
                    )
                )["data"]

                # check if issue has links
                if len(links) > 0:

                    # loop through links
                    for link in links:

                        # check attribute
                        if not hasattr(issue, link["link_type"]): setattr(issue, link["link_type"], list())

                        # add id to issue link type attribute
                        ids = getattr(issue, link["link_type"])
                        ids.append((link["id"], link["link_updated_at"]))

                        # set attribute
                        setattr(issue, link["link_type"], ids)

        return issues

    def nest(self, issues: list) -> dict:
        """
        Nest issues by parent/child link relationship (relates_to, blocks, is_blocked_by).

        Args:
            issues: (list): GitlabIssue classes where each represents a GitLab Issue

        Returns:
            A directional network representing the link relationship.
        """

        result = None

        # get link type lists
        blocking_issues = [d for d in issues if hasattr(d, "blocks")]
        blocked_issues = [d for d in issues if hasattr(d, "is_blocked_by")]

        # generate leaves
        link_leaves = [
            x for y in [
                [(d.id, i[0]) for i in d.relates_to]
                for d in issues
                if hasattr(d, "blocks")
            ] for x in y
        ]

        # generate roots
        link_roots = [
            (0, d.id) for d in issues
            if hasattr(d, "blocks") and
            d.id not in blocked_issues
        ]

        # combine list
        links = link_leaves + link_roots

        # check for links
        if len(links) > 0:

            # generate graph
            result = nx.DiGraph(links)

        return result
