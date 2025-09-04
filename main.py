


import logging
import os
from pathlib import Path
import shutil
from typing import Generator

from constants import COMMON_JUNK_FILENAMES, SYSTEM_JUNK_FILES
from constants import COMMON_MIME_TYPES_MOZILLA
from constants import EXCLUDE_DIRS_WINDOWS_COMMON

DEFAULT_MEDIA_FILE_EXTENSIONS = COMMON_MIME_TYPES_MOZILLA

DEFAULT_EXCLUDE_DIRS = EXCLUDE_DIRS_WINDOWS_COMMON

logger = logging.getLogger(__name__)

def scantree(path, yield_dirs=False) -> Generator[os.DirEntry[str], None, None]:
    """Recursively yield DirEntry objects for files (only) within the
    directory specified by `path`.

    Parameters
    ----------
    path : str or Path
        The root directory to scan.
    yield_dirs : bool, optional
        If True, also yield directory entries (not just files).

    Notes
    -----
    Source: `https://stackoverflow.com/a/33135143`.
    """
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            if yield_dirs:
                yield entry
            yield from scantree(entry.path, yield_dirs=yield_dirs)
        else:
            yield entry


def _delete_empty_directories(root_path):
    """Recursively delete empty directories under the specified root
    directory (returning a set of deleted directory paths).

    Notes
    -----
    Source: `https://stackoverflow.com/a/65624165`.
    """
    deleted = set()
    for current_dir, subdirs, files in os.walk(root_path, topdown=False):
        still_has_subdirs = False
        for subdir in subdirs:
            if os.path.join(current_dir, subdir) not in deleted:
                still_has_subdirs = True
                break
        if not any(files) and not still_has_subdirs:
            logger.info(f"Deleting empty directory: {current_dir}")
            os.rmdir(current_dir)
            deleted.add(current_dir)
    return deleted


def _extract_media_files(
        source_path: Path,
        dest_path: Path,
        extensions: set[str] | None = None,
        exclude_dirs: set[Path] | None = None,
        ) -> None:
    """
    Recursively extract (move) media files from `source_path` to
    `dest_path`, preserving directory structure.

    Parameters
    ----------
    source_path : Path
        The (top-level) source directory in which to search for media
        files.
    dest_path : Path
        The destination directory under which to place the extracted
        files.
    extensions : set[str] | None
        A set of file extensions (case insensitive) to consider as media
        files. If None, a default set of media file extensions will be
        used.
    exclude_dirs : set[Path] | None
        A set of directory paths (relative to `source_path`) to exclude
        from the search. If not specified, a default set of common
        system-only directories will be used.

    Notes
    -----
    Uses `os.scandir` for performance reasons (vs. eg. `pathlib`
    equivalent(s)).
    """
    if extensions is None:
        extensions = DEFAULT_MEDIA_FILE_EXTENSIONS
    if not source_path.is_dir():
        raise ValueError(
            f"Source path '{source_path}' is not a directory.")
    if not dest_path.is_dir():
        raise ValueError(
            f"Destination path '{dest_path}' is not a directory.")
    
    # Main Iteration Loop
    for file in scantree(source_path):
        rel_path = Path(file.path).relative_to(source_path)
        if exclude_dirs and any(
                rel_path.is_relative_to(excl_dir)
                for excl_dir in exclude_dirs):
            continue
        if file.name.lower().endswith(tuple(ext.lower() for ext in extensions)):
            dest_file_path = dest_path / rel_path
            dest_file_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Moving '{file.path}' to '{dest_file_path}'")
            os.rename(file.path, dest_file_path)

def _delete_common_junk_files(
        root_path: Path,
        junk_filenames: set[str] | None = None
        ) -> None:
    """Delete common junk files (e.g. Thumbs.db, .DS_Store) under the
    specified root directory.

    Parameters
    ----------
    root_path : Path
        The root directory under which to delete junk files.
    junk_filenames : set[str] | None
        A set of junk file names to delete. If None, a default set will
        be used.
    """
    if junk_filenames is None:
        junk_filenames = COMMON_JUNK_FILENAMES
    for entry in scantree(root_path):
        if entry.name in junk_filenames:
            logger.info(f"Deleting junk file: {entry.path}")
            os.remove(entry.path)

def _delete_windows_directories(
        root_path: Path
        ) -> None:
    """Find any `WINDOWS` directories (confirming any matches also
    contain a `system32` sub-directory) within `root_path`, and delete
    these.
    """
    for entry in scantree(root_path, yield_dirs=True):
        if entry.name == "WINDOWS" and entry.is_dir():
            system32_dir = Path(entry) / "system32"
            if system32_dir.is_dir():
                logger.info(f"Deleting Windows directory: {entry.path}")
                shutil.rmtree(entry.path)

def sanitise_dump_directory(
        dump_path: Path,
        extract_media_files_to: Path,
        media_file_extensions: set[str] | None = None,
        exclude_dirs: set[Path] | None = None,
        remove_common_junk_files: bool = False,
        remove_system_junk_files: bool = False,
        remove_windows_dirs: bool = False,
        remove_empty_dirs: bool = False,
        ) -> None:
    """
    Sanitize the specified dump directory by removing unwanted files and
    folders.

    Parameters
    ----------
    dump_path : Path
        `Path` to the dump directory to sanitize.
    extract_media_files_to : Path
        `Path` to the destination directory under which to place any
        extracted media files.
    media_file_extensions : set[str] | None
        A set of file extensions (case insensitive) to consider as media
        files. If None, a default set of media file extensions will be
        used.
    exclude_dirs : set[Path] | None
        A set of directory paths (relative to `dump_path`) to exclude
        from the search. If not specified, a default set of common
        system-only directories will be used.
    remove_common_junk_files : bool, default=True
        Toggle whether to remove common junk files (e.g. Thumbs.db,
        .DS_Store) from the dump directory.
    remove_system_junk_files : bool, default=True
        Toggle whether to remove system junk files (e.g. pagefile.sys)
        from the dump directory.
    remove_windows_dirs : bool, default=True
        Toggle whether to remove Windows directories (e.g. C:\WINDOWS)
        from the dump directory.
    remove_empty_dirs : bool, default=True
        Toggle whether to remove empty directories after sanitizing the
        dump directory.
    """

    # Remove WINDOWS directories
    if remove_windows_dirs:
        logger.info("Removing Windows directories...")
        _delete_windows_directories(
            root_path=dump_path
        )

    # Remove common junk files
    if remove_common_junk_files:
        logger.info("Removing common junk files...")
        _delete_common_junk_files(
            root_path=dump_path,
            junk_filenames=COMMON_JUNK_FILENAMES
        )

    # Remove system junk files
    if remove_system_junk_files:
        logger.info("Removing common junk files...")
        _delete_common_junk_files(
            root_path=dump_path,
            junk_filenames=SYSTEM_JUNK_FILES
        )

    # Run media file extraction
    _extract_media_files(
        source_path=dump_path,
        dest_path=extract_media_files_to,
        extensions=media_file_extensions,
        exclude_dirs=exclude_dirs,
    )

    # Remove empty directories
    if remove_empty_dirs:
        logger.info("Removing empty directories...")
        deleted_dirs = _delete_empty_directories(dump_path)
