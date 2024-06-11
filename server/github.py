from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter

from allauth.socialaccount.providers.github.provider import GitHubProvider


class GitHubOAuth2Adapter(GitHubOAuth2Adapter):

    provider_id = GitHubProvider.id


github_oauth2_adapter = GitHubOAuth2Adapter()