# Public Repository Hardening Baseline v0.1

Status: ACTIVE REPOSITORY-SIDE BASELINE  
Tracking Issue: #446

## 1. Purpose

Keep the repository public while reducing accidental leakage and repository-integrity risk **without changing the current project execution model**.

The canonical workflow remains:

```text
GitHub Issue
  -> short-lived lane branch
  -> PR
  -> deterministic validation
  -> accepted merge to main
```

This baseline does not alter Product or Knowledge semantics.

## 2. Non-interference constraint

Security controls must not require a second human operator for routine work and must not block the existing ChatGPT/GitHub execution path.

Do not introduce, without a later explicit governance decision:

- required human approvals greater than 0;
- required Code Owner review;
- required signed commits;
- merge queue;
- deployment gates;
- branch-name restrictions incompatible with existing lane names;
- automatic `push` workflow triggers;
- workflow write permissions;
- changes to the G8 standard public-runner model.

## 3. Repository-side controls

The repository root `.gitignore` blocks common local secret files, private keys, dependency directories, caches, editor state, and temporary files.

`COPYRIGHT.md` clarifies that:
- original project-authored material is not automatically open-licensed merely because the repository is public;
- third-party licenses and copyrights remain controlling for their material;
- full copyrighted source books are not intended for repository redistribution.

These controls do not modify runtime behavior.

## 4. Recommended GitHub main ruleset

Configure a ruleset targeting `main` with the following **non-disruptive** settings:

### Enable

- Require a pull request before merging.
- Required approvals: **0**.
- Block force pushes.
- Restrict deletion of the protected branch.

### Leave disabled for now

- Required approving reviews.
- Code Owner review requirement.
- Required signed commits.
- Merge queue.
- Required deployments.
- Mandatory external-review gates.

### Status checks

The current project already validates PRs under G8.

Do **not** make an additional status check mandatory at the platform-ruleset layer until it is confirmed that the exact check name is stable and that the requirement will not block the owner/connector path during GitHub Actions incidents.

The governance requirement to validate before accepted merge remains in force independently of this platform setting.

## 5. Actions safety

Existing automatic execution is limited to `pull_request` plus manual `workflow_dispatch`; automatic `push` triggers remain prohibited.

Workflow permissions should remain least-privilege. Current routine workflows are expected to use:

```yaml
permissions:
  contents: read
```

Any future workflow requiring write permission needs a bounded Governance Issue before enablement.

## 6. Secret handling

Never commit API keys, passwords, tokens, private keys, cookies, local credential stores, or user private data.

The repository owner should enable GitHub Secret Scanning and Push Protection in repository settings where available. These platform controls do not change the branch/PR development workflow.

If a secret is ever committed, adding it to `.gitignore` afterwards is insufficient. Revoke/rotate the credential first and then perform an explicit history-remediation procedure if needed.

## 7. Public-repository boundary

Public visibility means outsiders can read, clone, and fork material that has already been published. Repository security controls protect integrity and accidental disclosure; they cannot make published content secret.

Accordingly, future production-only credentials, private user data, hidden benchmark answers, and any deliberately confidential commercial assets must not be committed to this public repository.

## 8. Administration boundary

The current GitHub connector does not expose repository Ruleset/Branch Protection administration.

Therefore the ruleset in section 4 and GitHub Secret Scanning / Push Protection remain owner-side GitHub UI settings. Their absence must not be represented as completed until verified.
