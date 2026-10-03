#!/bin/bash
# Run by gemini-rtsw-ci/build_rpm.sh just before `dnf builddep`. The MinGW cross
# compilers (32-bit Windows side of the WoW64 build) are in EPEL, which needs
# CRB on EL9.
set -euo pipefail
dnf -y install epel-release dnf-plugins-core
dnf config-manager --set-enabled crb
