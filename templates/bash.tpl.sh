
# Array of chunks
chunks=(
{chunks}
)

# Join chunks and decode
b64=$(printf "%s" "${{chunks[@]}}")
echo "$b64" | base64 -d > {filename}

echo "Wrote to {filename}"
