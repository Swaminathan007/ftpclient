import ftplib

def connect_to_host(host, user, password, port):
    try:
        ftp = ftplib.FTP()
        ftp.connect(host, port)
        ftp.login(user=user, passwd=password)
        return ftp  # Return the FTP object for further operations
    except Exception as e:
        print(e)
        return None  # Return None if connection fails

def retrieve_files_and_dirs(ftp):
    files_and_dirs = []
    try:
        # Get a list of items in the current directory
        items = ftp.nlst()
        
        for item in items:
            # Try to change to the directory
            try:
                ftp.cwd(item)
                files_and_dirs.append((item, "Directory"))
                ftp.cwd('..')  # Change back to parent directory
            except ftplib.error_perm:
                files_and_dirs.append((item, "File"))  # If it fails, it's a file
                
    except Exception as e:
        print(e)
        
    return files_and_dirs  # Return the list of files and directories