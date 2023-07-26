#Write-Host "First Pass..."
#Get-ChildItem | Select-Object Name,CreationTime,Mode

#Write-Host "Second Pass..."
#Get-ChildItem | Select-Object Name,CreationTime,Mode | Sort-Object CreationTime -Descending

#Get-ChildItem | Rename-Item -NewName {$_.LastWriteTime.ToString("yyyy-MM-dd HH.mm.ss ddd") + ($_.Extension)}
#Get-ChildItem *.txt | Rename-Item -NewName {$_.CreationTime.ToString("yyyy-MM-dd__HH.mm.ss") + ($_.Extension)}

# StampMe.ps1
# param( [string] $fileName)

$fileNames = Get-ChildItem *.bat -Recurse

"List of names: $fileNames"
""
""

foreach ($fileName in $fileNames) {

    # Display the original name:
    "Original filename: $fileName"

    $fileObj = get-item $fileName

    # Get the date:
    $DateStamp = get-date -uformat "%Y-%m-%d_%H.%M.%S"
    # "date: $DateStamp"
    # File Extention:
    $extOnly = $fileObj.extension
    # "extension: $extOnly"

    $nameOnly = ""
    if ($extOnly.length -eq 0) {
        $nameOnly = $fileObj.Name
        # rename-item "$fileObj" "$nameOnly-$DateStamp"
    } else {
        $nameOnly = $fileObj.Name.Replace($fileObj.Extension,'')
        # rename-item "$fileName" "$nameOnly-$DateStamp$extOnly"
    }

    # Display the new name:
    "New filename: $nameOnly-$DateStamp$extOnly"
    ""
}