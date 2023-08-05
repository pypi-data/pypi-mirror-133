
_CWP = None

def client_with_project():
    global _CWP
    if _CWP is None:
        from google.cloud.client import ClientWithProject
        _CWP = ClientWithProject()
    return _CWP