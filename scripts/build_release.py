# ███╗   ██╗██████╗
# ████╗  ██║██╔══██╗
# ██╔██╗ ██║██║  ██║
# ██║╚██╗██║██║  ██║
# ██║ ╚████║██████╔╝
# ╚═╝  ╚═══╝╚═════╝
#
# ND (Non-Destructive) Blender Add-on
# Copyright (C) 2024 Tristan S. & Ian J. (HugeMenace)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ---
# Contributors: Tristo (HM)
# ---

import subprocess
import sys
import zipfile
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
PACKAGE_ROOT_NAME = "ND"

ROOT_DOTFILES = (".versionrc", ".gitignore", ".editorconfig")
EXCLUDED_EXTENSIONS = ("js", "md")
ROOT_IMAGE_EXTENSIONS = ("jpg", "jpeg", "png", "gif", "webp", "bmp", "tif", "tiff")


def get_version():
    manifest = (ROOT_DIR / "blender_manifest.toml").read_text()

    for line in manifest.splitlines():
        if line.strip().startswith("version"):
            return line.split("=", 1)[1].strip().strip('"')

    raise SystemExit("Unable to determine the version from blender_manifest.toml.")


def get_tracked_files():
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT_DIR,
        check=True,
        capture_output=True,
        text=True,
    )

    return [path for path in result.stdout.split("\0") if path]


def is_excluded(path):
    parts = path.split("/")
    name = parts[-1]
    extension = name.rsplit(".", 1)[-1].lower() if "." in name else ""

    if "__pycache__" in parts:
        return True

    if path.startswith(".github/") or path.startswith("scripts/"):
        return True

    if extension in EXCLUDED_EXTENSIONS:
        return True

    is_root_level = len(parts) == 1

    if is_root_level and name in ROOT_DOTFILES:
        return True

    if is_root_level and extension in ROOT_IMAGE_EXTENSIONS:
        return True

    return False


def build_release(output_path):
    files = sorted(path for path in get_tracked_files() if not is_excluded(path))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.unlink(missing_ok=True)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            archive.write(ROOT_DIR / path, f"{PACKAGE_ROOT_NAME}/{path}")

    return len(files)


def main():
    version = get_version()

    if len(sys.argv) > 1:
        output_path = Path(sys.argv[1]).resolve()
    else:
        output_path = ROOT_DIR / f"nd-{version}.zip"

    count = build_release(output_path)

    print(f"Created {output_path} — {count} files, version {version}.")


if __name__ == "__main__":
    main()
