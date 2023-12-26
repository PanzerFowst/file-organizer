#################################################
### Saves all files into an array and then    ###
### loops through all of them, renaming them  ###
### and creating new subdirectories based on  ###
### creation date.                            ###
###                                           ###
### @author:  Anthony Moriarty.               ###
### @created: 2023/05/30.                     ###
#################################################



#################################
## Configurable Options Below: ##
## Recommend running with      ##
## isReadOnly set to true      ##
## until satisfied with output ##
#################################

# Basepath / directory (set this to make the "home directory out of which everything is created."):
$basepath = "c:\Users\The Machine\Pictures"
$destinationpath = "c:\Users\The Machine\Pictures\Work Testing"

# Read Only (If true, just prints potential files to console without copying or moving the files):
$isReadOnly = $true

# Directory Creation (Should the script create folders if they don't exist?):
$isCreatingDirectories = $false
# Empty Directory Deletion (Should the script delete folders if they are empty?):
$isDeletingEmptyDirectories = $true
# Copy or Move file:
#   If true, script moves and modifies the original file.
#   If false, script copies files without modifying old file.
$isTouchingOriginalFiles = $true
# Add count string to file end:
#   Should the script add "@000" to the end in cases of same file names?
#   Example: file@000.txt, file@001.txt, file@002.txt, fileCOOL@000.txt
$isAddingCountString = $false
# Add datestrings to end of file (Should the script add a datestring to the file name?):
$isAddingDateStrings = $false


# -Recurse looks into all subdirectories.  Leave the option out to only look at current directory.
$AllChildren = Get-ChildItem -Exclude "*.ps1" -Recurse -Path "$basepath\Work Testing\" -Include "*.jpg"
# Filter down to only File Objects:
$files = $AllChildren | Where-Object { !$_.PSisContainer }
$num = 1
"List of files:"
foreach ($file in $files) {
    "$num) $file"
    $num++
}
"`n`n`n"


$num = 1
# Loop through all the files:
foreach ($file in $files) {

    # Display the original name / path:
    $fileObj = Get-Item $file
    # "Original file: $fileObj"

    # Current Date Data:
    # $CurrentDate = Get-Date -uformat "%Y-%m-%d_%H.%M.%S"
    # $CurrentYear = Get-Date -uformat "%Y"
    # $CurrentMonth = Get-Date -uformat "%m"
    # $CurrentDay = Get-Date -uformat "%d"
    # "Date Stamp: $CurrentDate"
    # Creation Date Data:
    # # $CreationDate = $fileObj.CreationTime.DateTime
    # $CreationYear = $fileObj.CreationTime.Year
    # $CreationMonth = $fileObj.CreationTime.Month
    # $CreationDay = $fileObj.CreationTime.Day
    # $CreationTimeOfDay = $fileObj.CreationTime.TimeOfDay
    # "Creation Date: $CreationDate"





    # TODO: Clean up this code chunk...
    $shell = New-Object -ComObject Shell.Application
    $dir = $shell.NameSpace( $fileObj.Directory.FullName )
    $file = $dir.ParseName( $fileObj.Name )

    # First see if we have Date Taken, which is at index 12
    $index = 12
    $value = ($dir.GetDetailsof($file, $index) -creplace '\P{IsBasicLatin}')# -replace "`u{200E}") -replace "`u{200F}"
    # $value = "11/2/2022 9:24 AM"
    # $date = Get-Date-Property-Value $fileObj 12
    # "date before: $value"
    if ($value -and $value -ne '') {

        $date = [DateTime]::ParseExact($value, "g", $null)

    }
    else {
        $date = $null
        # If we don't have Date Taken, then find the oldest date from all date properties
        0..287 | ForEach-Object {
            $name = $dir.GetDetailsof($dir.items, $_)

            if ( $name -match '(date)|(created)') {

                # Only get value if date field because the GetDetailsOf call is expensive
                $tmp = ($dir.GetDetailsof($file, $_) -creplace '\P{IsBasicLatin}')
                if ($tmp -and $tmp -ne '') {
                    $tmp = [DateTime]::ParseExact($tmp, "g", $null)
                }
                else {
                    $tmp = $null
                }
                if ( ($null -ne $tmp) -and (($null -eq $date) -or ($tmp -lt $date))) {
                    $date = $tmp
                }
            }
        }
    }
    # "date after: $date"
    $CreationYear = $date.Year
    $CreationMonth = $date.Month
    $CreationDay = $date.Day
    $CreationTimeOfDay = $date.TimeOfDay





    # File Extention:
    $extOnly = $fileObj.Extension
    # "Extension: $extOnly"

    # Path / Directory:
    $Year_Str = ([string]$CreationYear).PadLeft(4, '0')
    $Month_Str = ([string]$CreationMonth).PadLeft(2, '0')
    $Day_Str = ([string]$CreationDay).PadLeft(2, '0')
    $Time_Str = ([string]$CreationTimeOfDay)
    # Take off the milliseconds with SubString if it exists:
    if ($Time_Str -contains '.') {
        $Time_Str = $Time_Str.Substring(0, $Time_Str.IndexOf('.'))
    }
    $Time_Str = $Time_Str.Replace(':', ';')
    # Used the '#' as a special delimiter that will be replaced with an '_' because of the variable names:
    $Date_Str = "$Year_Str-$Month_Str-$Day_Str#$Time_Str"
    $Date_Str = $Date_Str.Replace('#', '__')
    # Finally Create the new Path:
    $newPath = "$destinationpath\$Year_Str-$Month_Str\$Year_Str-$Month_Str-$Day_Str\"


    # File Renaming:
    $nameOnly = $fileObj.Name
    $oldPath = $fileObj.PSParentPath
    # Remove extention:
    if ($fileObj.Extension.length -gt 0) {
        $nameOnly = $fileObj.Name.Replace($fileObj.Extension, '')
    }
    # Grab name without "@###" on the end:
    if ($nameOnly.IndexOf('@') -gt 0) {
        $nameOnly = $nameOnly.Substring(0, $nameOnly.IndexOf('@'))
    }
    # $nameOnly = 'something'


    if ($isAddingDateStrings) {

        # "nameOnly: $nameOnly`t`tDate_Str: $Date_Str"
        # Some test stuff to see if need to rename files:
        if ($nameOnly -match $Date_Str) {
            # "Name already contains created date!  Skip renaming process..."
            $Name_Date_Str = "$nameOnly"
        }
        else {
            $Name_Date_Str = "$nameOnly---$Date_Str"
        }

    }
    else {
        $Name_Date_Str = "$nameOnly"
    }

    if ($isAddingCountString) {

        # Continue looping through names until finding a file:
        $count = 0
        do {
            $count_str = ([string]$count).PadLeft(3, '0')
            $newName = "$Name_Date_Str@$count_str$extOnly"
            # "New Location: $newPath$newName"
            $count++

        } while (Test-Path "$newPath$newName")

    }
    else {
        $newName = "$nameOnly$extOnly"
    }

    # Display the new path and name:
    "Item #$num`:"
    "New path: $newPath"
    "New filename: $newName"


    ######################################################################################
    ####################  ACTUAL FILE MODIFICATION BELOW THIS POINT!  ####################
    ######################################################################################

    $num++

    if (!($isReadOnly)) {

        # Directory Creation:
        if ($isCreatingDirectories -and !(Test-Path $newPath)) {

            "Path doesn't exist!  Creating path..."
            New-Item -ItemType Directory -Path "$newPath"
        }

        # Copy/Rename/Move file:
        if ($isTouchingOriginalFiles) {

            "Renaming file..."
            Rename-Item "$fileObj" "$newname"
            "Moving file..."
            Move-Item -Path "$oldPath\$newName" -Destination "$newPath"

        }
        else {

            "Copying file..."
            Copy-Item "$fileObj" "$newPath$newName"
        }

        # Change File Attributes after the fact (make sure to check that $CreationDate is uncommented above):
        # (Get-Item "$newPath$newName").CreationTime=$CreationDate #("18 February 2023 02:08:23")
        # (Get-Item "$newPath$newName").LastWriteTime=("16 January 2022 11:00:00")
    }

    # Extra space between loop iterations:
    "`n"
}

# Credit: https://www.delftstack.com/howto/powershell/powershell-delete-empty-folders/
if ($isDeletingEmptyDirectories) {
    do {
        $fetchedDirList = Get-ChildItem $basepath -Directory -Recurse
        # (The -Force flag looks for hidden files and folders.)
        $emptyDirectoryList = $fetchedDirList | Where-Object { (Get-ChildItem $_.fullName -Force).count -eq 0 }
        $finalListToRemove = $emptyDirectoryList | Select-Object -ExpandProperty FullName
        $finalListToRemove | ForEach-Object { Remove-Item $_ }
    } while ($finalListToRemove.count -gt 0)
}


# Final output:
"`n`n******************************************************************************`n"

if ($isCreatingDirectories) {
    "Potentially new directories created!"
}
else {
    "Did not create any directories."
}

if ($isDeletingEmptyDirectories) {
    "Deleted all empty folders in `"$basepath\`"!"
}
else {
    "Did not check to delete empty directories in `"$basepath\`"."
}

# For spacing:
""

if ($isReadOnly) {

    "Did not change any files."

    if ($isTouchingOriginalFiles) {
        "Would have moved files to the above locations..."
    }
    else {
        "Would have copied files to the above locations..."
    }

}
else {

    if ($isTouchingOriginalFiles) {
        "Moved files to the above locations..."
    }
    else {
        "Copied files to the above locations..."
    }
}

# For spacing:
""

if ($isAddingCountString) {
    "Added count strings (ex: file@000.txt) to files."
}

if ($isAddingDateStrings) {
    "Added date strings (ex: file---2023-06-01__10;12;46.09325.txt)"
}

"`n`n"
