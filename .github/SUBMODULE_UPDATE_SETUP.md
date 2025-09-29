# Metashade Submodule Auto-Update Setup

This document explains how to set up automatic updates of the `metashade` submodule when changes are pushed to `metashade/main`.

## Overview

The workflow `.github/workflows/update-metashade-submodule.yml` automatically creates pull requests to update the metashade submodule whenever new commits are pushed to the main metashade repository.

## Trigger Methods

The workflow can be triggered in three ways:

### 1. Repository Dispatch (Recommended)
This method allows the metashade repository to trigger updates in this repository via GitHub's API.

#### Setup in metashade repository:
Add a workflow in `metashade/metashade` repository (`.github/workflows/notify-gltf-sample.yml`).
A complete example is provided in this repository at `.github/metashade-repository-workflow-example.yml`.

#### Required Secret:
- In the `metashade/metashade` repository, add a secret named `GLTF_SAMPLE_DISPATCH_TOKEN`
- This should be a GitHub Personal Access Token with `repo` scope
- The token should be created by a user with write access to `metashade/metashade-glTFSample`

### 2. Manual Trigger
The workflow can be triggered manually from the GitHub Actions tab:
- Go to Actions → Update Metashade Submodule → Run workflow
- Optionally specify a specific commit/branch/tag to update to

### 3. Scheduled Updates
The workflow runs daily at 02:00 UTC to check for updates automatically.

## Workflow Behavior

1. **Checks current state**: Compares the current submodule commit with the latest from metashade/main
2. **Updates if needed**: Only creates a PR if there are actual changes
3. **Creates PR**: Automatically creates a pull request with:
   - Descriptive title and body
   - Commit information from the metashade update
   - Link to the specific changes
4. **Runs CI**: The existing CI pipeline validates the changes
5. **Auto-cleanup**: The feature branch is automatically deleted after PR merge/close

## Permissions

The workflow requires:
- `contents: write` - to update submodules and create commits
- `pull-requests: write` - to create pull requests

These are provided by the default `GITHUB_TOKEN`.

## Customization

### Changing Update Frequency
Edit the `schedule` section in the workflow file:
```yaml
schedule:
  - cron: '0 2 * * *'  # Daily at 02:00 UTC
```

### Targeting Different Branches
By default, the workflow updates to `metashade/main`. To target a different branch:
1. Update the `.gitmodules` file to specify the branch
2. Or use the manual trigger with a specific ref

### Modifying PR Template
Edit the `body` section in the "Create Pull Request" step to customize the PR description.

## Troubleshooting

### PR Not Created
- Check if there are actually new commits in metashade/main
- Verify the workflow has the necessary permissions
- Check the Actions logs for error messages

### Submodule Update Failures
- Ensure the metashade repository is accessible
- Check if there are conflicts in the submodule
- Verify the target branch/commit exists

### Token Issues (Repository Dispatch)
- Ensure the dispatch token has correct permissions
- Verify the token hasn't expired
- Check that the repository names are correct