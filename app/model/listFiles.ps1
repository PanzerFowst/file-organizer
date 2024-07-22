param(
    [ValidateNotNullOrEmpty()]
    [ValidateScript({
        if (-Not ($_ | Test-Path)) {
            throw "File or folder ($_) does not exist."
        }
        return $true
    })]
    [System.IO.DirectoryInfo]$input_path,
    [string]$recursive = "false", # default value if not assigned
    $envname
)

# Convert string boolean values to actual Booleans
[bool]$recursive = [System.Convert]::ToBoolean($recursive)


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
