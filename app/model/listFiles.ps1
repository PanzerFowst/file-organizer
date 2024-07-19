param(
    [ValidateNotNullOrEmpty()]
    [ValidateScript({
        if (-Not ($_ | Test-Path)) {
            throw "File or folder ($_) does not exist."
        }
        return $true
    })]
    [System.IO.DirectoryInfo]$input_path,
    [System.IO.DirectoryInfo]$output_path,
    [string]$recursive = "false", # TODO: Add this option later...
    [string]$is_safe_mode = "true", # default value if not assigned
    [string]$is_creating_new_directories = "false",
    [string]$is_deleting_empty_directories = "false",
    [string]$is_moving_files = "false",
    [string]$is_adding_count_str = "false",
    [string]$is_adding_date_str = "false",
    $envname
)

# Convert string boolean values to actual Booleans
[bool]$recursive = [System.Convert]::ToBoolean($recursive)
[bool]$is_safe_mode = [System.Convert]::ToBoolean($is_safe_mode)
[bool]$is_creating_new_directories = [System.Convert]::ToBoolean($is_creating_new_directories)
[bool]$is_deleting_empty_directories = [System.Convert]::ToBoolean($is_deleting_empty_directories)
[bool]$is_moving_files = [System.Convert]::ToBoolean($is_moving_files)
[bool]$is_adding_count_str = [System.Convert]::ToBoolean($is_adding_count_str)
[bool]$is_adding_date_str = [System.Convert]::ToBoolean($is_adding_date_str)

Write-Host "`n"
Write-Host "Looking in '$input_path'..."
Write-Host "Output Path: '$output_path'..."
Write-Host "Recursive Search = $recursive"
Write-Host "Safe Mode = $is_safe_mode"
Write-Host "New Directories = $is_creating_new_directories"
Write-Host "Deleting Empty = $is_deleting_empty_directories"
Write-Host "Moving Files = $is_moving_files"
Write-Host "Adding Count = $is_adding_count_str"
Write-Host "Adding Date = $is_adding_date_str"


# -Recurse looks into all subdirectories.  Leave the option out to only look at current
# directory.  The results are piped into Where-Object which filters by file extension.
$AllChildren = if ($recursive) {
    Get-ChildItem -Exclude "*.ps1" -Path $input_path -Recurse
} else {
    Get-ChildItem -Exclude "*.ps1" -Path $input_path
}
# Filter down to only File Objects:
$files = $AllChildren | Where-Object { !$_.PSisContainer }
$num = 1
if ($files.count -gt 0) {
    "List of files:"
    foreach ($file in $files) {
        "$num) $file"
        $num++
    }
} else {
    "No files were found.  The file list is empty."
}
"`n`nDone!!!"
