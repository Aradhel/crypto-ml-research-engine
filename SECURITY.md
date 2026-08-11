# Security policy

This repository must never contain exchange credentials, private trading data,
IP addresses, logs, databases or serialized production models.

If you discover a credential or sensitive artifact, do not open a public issue.
Remove the exposed credential at its provider, rotate it immediately and purge it
from Git history before publishing again.

The demo does not need credentials. Any pull request adding authenticated
exchange access is outside the scope of this public project.

