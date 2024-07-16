param(
    [ValidateNotNullOrEmpty()]
    [ValidateScript({
        if (-Not ($_ | Test-Path)) {
            throw "File or folder ($_) does not exist."
        }
        return $true
    })]
    $input_path,
    $output_path,
    $recursive = $true, # TODO: Add this option later...
    $is_safe_mode = $true, # default value if not assigned
    $is_creating_new_directories = $false,
    $is_deleting_empty_directories = $false,
    $is_moving_files = $false,
    $is_adding_count_str = $false,
    $is_adding_date_str = $false,
    $envname
)
Write-Host "Looking in '$input_path'..."
Write-Host "Output Path: '$output_path'..."
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
