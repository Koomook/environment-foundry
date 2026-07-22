# Private data plane policy

This directory contains policy only. Private payload must not be committed.

Store person/company messages, recordings, faces, contacts, credentials, contracts, customer records, and operational exports in an approved access-controlled system outside Git. Git may contain only:

- an opaque locator that reveals no sensitive payload;
- purpose and rights category;
- owner and review date;
- retention/revocation state;
- a content hash when safe;
- an aggregate or redacted artifact explicitly cleared for the lab.

Local payload belongs under `private-plane/payload/`, which is ignored. `internal-only` is not permission to commit raw private data.
