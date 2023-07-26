$test1 = "someFile-copy-2023-05-30_22.48.34.bat"
$sub = "2023-05-30_22.48.34"
# Outputs True/False:
$test1 -match $sub



$files = Get-ChildItem -Exclude "*.ps1" -Recurse -Path ".\" #*.bat"
"List of files:"
foreach ($file in $files) {"$file"}
""
""
""
$filesOnly = $files | Where-Object { !$_.PSisContainer }
"List of files:"
foreach ($file in $filesOnly) {"$file"}
""
""
""
