from filepath_config import readFileList, getHash
from logger import monitorLogger
from notifier import fileChange

# This function compares two hash strings and returns True if they match, False if not
def compareHash(current_hash: str, saved_hash: str) -> bool:
    return current_hash == saved_hash

# This function monitors all file paths listed in file_list.json
# It compares the current hash of the file with the saved hash and logs + alerts if any changes are found
def monitorFile():
    try:
        file_dict = readFileList()  # { "path": "hash" }
        
        if not file_dict:
            return

        for filepath, saved_hash in file_dict.items():
            current_hash = getHash(filepath)

            if current_hash is None:
                msg = f"Could not read or hash the file: {filepath}"
                monitorLogger(msg)
                fileChange(msg)
                continue

            if not compareHash(current_hash, saved_hash):
                msg = f"File altered: {filepath}"
                monitorLogger(msg)
                fileChange(msg)

    except Exception as e:
        error_msg = f"File Monitoring encountered an error: {str(e)}"
        monitorLogger(error_msg)
        fileChange(error_msg)