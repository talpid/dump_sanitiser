

import argparse
import logging
from pathlib import Path
from venv import logger

from main import sanitise_dump_directory

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "Sanitise a whole-drive dump directory (extract media "
            "files, remove empty directories).")
    )
    parser.add_argument(
        "--dump_path", "-d",
        required=True,
        type=Path,
        help="The (top-level) source directory in which to search for "
             "media files.")
    parser.add_argument(
        "--extract_media_files_to", "-e",
        required=True, # TODO: allow None -> don't extract
        type=Path,
        help="The destination directory under which to place the "
             "extracted files.")
    parser.add_argument(
        "--remove_common_junk_files", "-j",
        action="store_true",
        default=True,
        help="Whether to remove common junk files (e.g. Thumbs.db, "
             ".DS_Store).")
    parser.add_argument(
        "--remove_system_junk_files",
        action="store_true",
        default=True,
        help="Whether to remove system junk files (e.g. pagefile.sys) "
             "from the dump directory.")
    parser.add_argument(
        "--remove_empty_dirs", "-r",
        action="store_true",
        default=True,
        help="Whether to remove empty directories after extraction.")
    parser.add_argument(
        "--extensions",
        type=str,
        nargs="+",
        default=None,
        help="A list of file extensions (case insensitive) to consider "
             "as media files. If not provided, a default set of media "
             "file extensions will be used.")
    parser.add_argument(
        "--exclude_dirs",
        type=Path,
        nargs="+",
        default=None,
        help="A list of directory paths (relative to `dump_path`) to "
             "exclude from the search. If not specified, a default set of "
             "common system-only directories will be used.")
    parser.add_argument(
        "--make_dest_ok",
        action="store_true",
        default=False,
        help="Whether to create the destination directory if it doesn't exist.")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",  # Set a default level
        help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=None,
        help="Optional path to which to write logs (if not specified, logs "
             "will not be written to a file)."
        )

    args = parser.parse_args()

    log_level = getattr(logging, args.log_level.upper(), logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    if args.log_file:
        file_handler = logging.FileHandler(args.log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.info(f"Starting sanitisation process for dump at {args.dump_path}")

    if args.make_dest_ok:
        args.extract_media_files_to.mkdir(parents=True, exist_ok=True)

    sanitise_dump_directory(
        dump_path=args.dump_path,
        extract_media_files_to=args.extract_media_files_to,
        media_file_extensions=set(args.extensions) if args.extensions else None,
        exclude_dirs=set(args.exclude_dirs) if args.exclude_dirs else None,
        remove_empty_dirs=args.remove_empty_dirs
    )
    