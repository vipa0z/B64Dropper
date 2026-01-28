
# Array of base64 chunks
$chunks = @(
{chunks}
)

# Join chunks into single string
$b64 = $chunks -join ""

# Convert base64 string to byte array
$payload = [System.Convert]::FromBase64String($b64)

# Write bytes to file
[System.IO.File]::WriteAllBytes("{filename}", $payload)

Write-Host "Wrote $($payload.Length) bytes to {filename}"
