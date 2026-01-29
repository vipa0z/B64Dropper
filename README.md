# B64Dropper

## Description

B64Dropper facilitates **Living off the Land (LotL)** by converting binaries into polyglot scripts (Java, Python, Bash, etc.) with embedded Base64 payloads. It enables tool transfers using only standard libraries, bypassing the need for outbound connections.
In simpler terms, this is useful when you have access to script consoles or features that allow programmatic interaction with the host, but are limited to basic shell commands. It allows you to transfer binaries/redteam tools through standard script code (like Java or Python) to reconstruct the executable on the target.


## History 
This tool was originally developed as a Proof of Concept (POC) to exploit vulnerabilities in DevOps environments where outgoing connections were completely blocked and all i had was a script console, other upload techniques were not possible.

When delivering larger binaries (like `mimikatz`, `winpeas`, or C2 agents), script interpreters often have limits on string literal lengths. B64Dropper automatically handles this by splitting the payload into chunks (default 6000 chars).

initial targets included:

- **ShellBeans**: Exploiting Java deserialization or command injection flaws where only blind execution was available.
- **Jenkins**: Leveraging Groovy script console or agent execution to drop tooling on build nodes.
- **Liferay**: Used in POCs targeting Liferay portal script console to drop bindshells

## POC
![poc](poc.gif)

## Usage 

```text
usage: b64dropper.py [-h] [-l {groovy,java,js,python,powershell,bash,go,csharp,cpp}] [-o OUTPUT]
                     [-f FILENAME] [-s CHUNK_SIZE]
                     input_file

Convert a binary file to a base64 dropper script in various languages.

positional arguments:
  input_file            Path to the input binary file (e.g. tool.exe)

options:
  -h, --help            show this help message and exit
  -l {groovy,java,js,python,powershell,bash,go,csharp,cpp}, --language {groovy,java,js,python,powershell,bash,go,csharp,cpp}
                        Target programming language for the dropper script
  -o OUTPUT, --output OUTPUT
                        Output file (for script) or directory (for legacy chunks)
   -p PATH, --path PATH  Path where the file will be created on the target system

                        Name of the file to be created on the target system (used in script mode)
  -s CHUNK_SIZE, --chunk-size CHUNK_SIZE
                        Length of each chunk string (default: 6000)
```


## EXAMPLE

Generate a dropper for a small tool (e.g., `nc.exe`) to be executed via a Python interpreter on the target:

```bash
python3 b64dropper.py nc.exe -l groovy -f nc.exe -o nc_dropper_script.groovy
# copy to your clipboard
cat deploy_nc.groovy | xclip -selection clipboard -i
```

---

