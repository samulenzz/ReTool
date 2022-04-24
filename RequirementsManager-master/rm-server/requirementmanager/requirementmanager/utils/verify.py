from requirementmanager.http_client import projectmanager_http_client


def verify_project_user_role_access(project_id: str,
                                    username: str,
                                    access: str) -> bool:
    return projectmanager_http_client.user_role_verify(
        project_id, username, access
    )
