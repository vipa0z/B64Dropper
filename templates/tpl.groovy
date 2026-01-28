
import java.util.Base64
import java.nio.file.Files
import java.nio.file.Paths

// List of base64 chunks
def chunks = [
{chunks}
]

// Join chunks into a single string
def b64 = chunks.join('')

// Decode base64 string to byte array
def payload = Base64.decoder.decode(b64)

// Define output path
def dest = Paths.get("{filename}")

// Write bytes to file
Files.write(dest, payload)

println "Wrote ${{payload.length}} bytes to ${{dest}}"
