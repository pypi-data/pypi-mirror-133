from github3.orgs import ShortOrganization

from zen_core.handlers.access_controlled_git_object import AccessControlledGitObject
from zen_core.handlers.git_repo import GitRepo
from zen_core.handlers.git_team import GitTeam
from zen_core.handlers.git_user import GitUser
from zen_core.parsing.org_config import OrgConfig
from zen_core.parsing.team_config import TeamConfig


class GitOrg(AccessControlledGitObject):

    def __init__(self, git_org: ShortOrganization):
        super().__init__(git_org)

    def login(self):
        return self._git_object.login

    def grant_access(self, username, role='member'):
        current_permission = self.permission_for(username)
        if current_permission != 'admin':
            self._git_object.add_or_update_membership(username, role)

    def revoke_access(self, username):
        self._git_object.remove_membership(username)

    def as_dict(self):
        return self._git_object.as_dict()

    def configuration(self):
        members = [m.login() for m in self.members('member')]
        admins = [m.login() for m in self.members('admin')]
        current_teams = self.teams()
        current_team_configuration = {}
        for team in current_teams:
            team_members = [m.login() for m in team.members(role='member')]
            team_admins = [m.login() for m in team.members(role='maintainer')]

            repos = {repo.full_name(): repo.permission_for_team(team.login()) for repo in team.repositories()}
            current_team_configuration[team.login()] = TeamConfig(team_members, team_admins, repos)

        return OrgConfig(self.login(), members, admins, current_team_configuration)

    def members(self, role=None):
        return [GitUser(m) for m in self._git_object.members(role=role)]

    def permission_for(self, username):
        members = [m.login() for m in self.members(role='member')]
        admins = [m.login() for m in self.members(role='admin')]
        if username in admins:
            return 'admin'
        elif username in members:
            return 'member'
        else:
            return None

    def create_team(self, name, repos=None, permission='pull'):
        if not repos:
            repos = []
        return GitTeam(self._git_object.create_team(name, repo_names=repos, permission=permission, privacy='closed'))

    def repositories(self):
        return [GitRepo(r) for r in self._git_object.repositories()]

    def teams(self):
        return [GitTeam(t) for t in self._git_object.teams()]

    def team(self, name):
        for t in self.teams():
            if t.name() == name:
                return t
        return None

    def __repr__(self):
        return f'org::{self.login()}'
