
import java.util.Base64;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.IOException;

public class tpl {
    public static void main(String[] args) throws IOException {
        // Array of base64 chunks
        String[] chunks = {
                "{chunks}"
        };

        // Reconstruct full base64 string efficiently
        StringBuilder b64 = new StringBuilder();
        for (String chunk : chunks) {
            b64.append(chunk);
        }

        // Decode base64 to bytes
        byte[] payload = Base64.getDecoder().decode(b64.toString());

        // Write bytes to target file
        Files.write(Paths.get("{filename}"), payload);

        System.out.println("Wrote " + payload.length + " bytes to {filename}");
    }
}
