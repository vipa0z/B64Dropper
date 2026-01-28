using System;
using System.IO;
using System.Text;

class Dropper
{{
    static void Main()
    {{
        // Array of base64 chunks
        string[] chunks = {{
{chunks}
        }};

        // Efficiently build the full base64 string
        StringBuilder b64 = new StringBuilder();
        foreach (string chunk in chunks)
        {{
            b64.Append(chunk);
        }}

        // Convert base64 string to byte array
        byte[] payload = Convert.FromBase64String(b64.ToString());
        
        // Write byte array to file
        File.WriteAllBytes("{filename}", payload);
        
        Console.WriteLine($"Wrote {{payload.Length}} bytes to {filename}");
    }}
}}
