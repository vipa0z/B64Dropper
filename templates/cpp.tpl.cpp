#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>

// Simple Base64 decoder function (dependency-free)
static const std::string base64_chars = 
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
             "abcdefghijklmnopqrstuvwxyz"
             "0123456789+/";

static inline bool is_base64(unsigned char c) {{
  return (isalnum(c) || (c == '+') || (c == '/'));
}}

// Decodes a base64 encoded string into a vector of bytes
std::vector<unsigned char> base64_decode(std::string const& encoded_string) {{
  int in_len = encoded_string.size();
  int i = 0;
  int j = 0;
  int in_ = 0;
  unsigned char char_array_4[4], char_array_3[3];
  std::vector<unsigned char> ret;

  while (in_len-- && ( encoded_string[in_] != '=') && is_base64(encoded_string[in_])) {{
    char_array_4[i++] = encoded_string[in_]; in_++;
    if (i ==4) {{
      for (i = 0; i <4; i++)
        char_array_4[i] = base64_chars.find(char_array_4[i]);

      char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
      char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
      char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

      for (i = 0; (i < 3); i++)
        ret.push_back(char_array_3[i]);
      i = 0;
    }}
  }}

  if (i) {{
    for (j = i; j <4; j++)
      char_array_4[j] = 0;

    for (j = 0; j <4; j++)
      char_array_4[j] = base64_chars.find(char_array_4[j]);

    char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
    char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
    char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

    for (j = 0; (j < i - 1); j++) ret.push_back(char_array_3[j]);
  }}

  return ret;
}}

int main() {{
    // Vector of base64 chunks
    std::vector<std::string> chunks = {{
{chunks}
    }};

    // Combine chunks into single stream
    std::stringstream b64_ss;
    for (const auto& chunk : chunks) {{
        b64_ss << chunk;
    }}

    // Decode to binary data
    std::vector<unsigned char> payload = base64_decode(b64_ss.str());
    
    // Write binary data to file
    std::ofstream out("{filename}", std::ios::binary);
    out.write(reinterpret_cast<const char*>(payload.data()), payload.size());
    out.close();

    std::cout << "Wrote " << payload.size() << " bytes to {filename}" << std::endl;
    return 0;
}}
