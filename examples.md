
# On CAERNARFON (Unraid)

## Sanitise "Brown_*_HDD"

```
python /longmore/scott_storage/vscode/dump_sanitiser/cli.py \
    --dump_path /longmore/erin_backup/Manual_Backups/Brown_SMSNG_HDD \
    --extract_media_files_to /longmore/erin_backup/Manual_Backups/Brown_SMSNG_HDD_MIME_files \
    --log-file /longmore/erin_backup/Manual_Backups/Brown_SMSNG_HDD_sanitise.log \
    --log-level DEBUG
```

```
python /longmore/scott_storage/vscode/dump_sanitiser/cli.py \
    --dump_path /longmore/erin_backup/Manual_Backups/Brown_WD_HDD \
    --extract_media_files_to /longmore/erin_backup/Manual_Backups/Brown_WD_HDD_MIME_files \
    --log-file /longmore/erin_backup/Manual_Backups/Brown_WD_HDD_sanitise.log \
    --log-level DEBUG
```

```
python /longmore/scott_storage/vscode/dump_sanitiser/cli.py \
    --dump_path /mnt/disks/Jenny_Disk/Misc_Brown_BU/Brown_SMSNG_HDD \
    --extract_media_files_to /mnt/disks/Jenny_Disk/Misc_Brown_BU/Brown_SMSNG_HDD_MIME_files \
    --make_dest_ok \
    --log-file /mnt/disks/Jenny_Disk/Misc_Brown_BU/Brown_SMSNG_HDD_sanitise.log \
    --log-level DEBUG
```

```
python /longmore/scott_storage/vscode/dump_sanitiser/cli.py \
    --dump_path /mnt/disks/Jenny_Disk/Misc_Brown_BU/Brown_WD_HDD \
    --extract_media_files_to /mnt/disks/Jenny_Disk/Misc_Brown_BU/Brown_WD_HDD_MIME_files \
    --make_dest_ok \
    --log-file /mnt/disks/Jenny_Disk/Misc_Brown_BU/Brown_WD_HDD_sanitise.log \
    --log-level DEBUG
```
