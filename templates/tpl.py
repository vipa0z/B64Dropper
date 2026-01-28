
import base64
import os

# List of base64 chunks
chunks = [
{chunks}
]

# Join chunks and decode
b64 = "".join(chunks)
payload = base64.b64decode(b64)

# Write decoded bytes to file
with open("{filename}", "wb") as f:
    f.write(payload)

print(f"Wrote {{len(payload)}} bytes to {filename}")
