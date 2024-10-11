import base64




def decode_encoded_file_path(encoded_file_path: str):
    """
    decode encoded file provided
    """
    decoded_file = base64.b64decode(encoded_file_path)
    with open("service_account_key.json", 'w', encoding="UTF-8") as j_file:
        j_file.write(decoded_file.decode("utf-8"))

