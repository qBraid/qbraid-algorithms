#!/bin/bash

# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

################################################################################
# Description:
# Script for creating development package builds. It temporarily checks out
# a new branch, modifies the `package.json` file to reflect the provided
# development version, and then triggers the build process.
#
# Usage:
#   ./create_dev_build.sh <DEV_VERSION> <OUT_DIR>
#
# Arguments:
#   DEV_VERSION: The development version string to use for the build.
#   OUT_DIR: The directory where the built packages will be stored.
#
# Example:
#   ./create_dev_build.sh "1.0.0-a1" "/path/to/output_directory"
################################################################################

set -e

# Check for required arguments
if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <DEV_VERSION> <OUT_DIR>"
    exit 1
fi

DEV_VERSION="${1}"
OUT_DIR="${2}"


# Constants
REPO_DIR=$(git rev-parse --show-toplevel)
PYPROJECT_TOML_PATH="${REPO_DIR}/pyproject.toml"
TMP_BRANCH="tmp_build_branch_$(date "+%Y%m%d%H%M%S")"

# Cleanup function
cleanup() {
    echo "Cleaning up..."

    # If the TMP_BRANCH exists, checkout the original branch and delete TMP_BRANCH
    if git rev-parse --verify "${TMP_BRANCH}" >/dev/null 2>&1; then
        git checkout HEAD -- "${PYPROJECT_TOML_PATH}" 2>/dev/null
        git checkout - 2>/dev/null
        git branch -D "${TMP_BRANCH}" 2>/dev/null
    else
        git checkout HEAD -- "${PYPROJECT_TOML_PATH}" 2>/dev/null
    fi
}

# Use trap to ensure cleanup runs on exit
trap cleanup EXIT

# Check if temporary branch name already exists
if git rev-parse --verify "${TMP_BRANCH}" >/dev/null 2>&1; then
    echo "Temporary branch name already exists. Exiting for safety."
    exit 1
fi

# Create and checkout temporary branch
echo "Creating and checking out temporary branch: ${TMP_BRANCH}"
git checkout -b "${TMP_BRANCH}"

# Check if toml-cli is installed
if ! command -v toml &> /dev/null
then
    echo "toml-cli could not be found. Please install toml-cli to use this script."
    exit 1
fi

# Update the version in the version file
echo "Setting version to ${DEV_VERSION}"
toml set "$PYPROJECT_TOML_PATH" "project.version" "$DEV_VERSION" > tmp.$$.toml && mv tmp.$$.toml "$PYPROJECT_TOML_PATH"

# Check if `build` module is installed
if ! python -c "import build" 2>/dev/null; then
    echo "'build' module is not installed. Please install it with 'pip install build'."
    exit 1
fi

# Build the project
echo "Building the project..."
python -m build --outdir "${OUT_DIR}"

echo "Done."