import requests
import io
import zipfile
import tarfile
import os
import platform

system = platform.system().lower()

#Download mitm proxy in zip format to extract the mitmdump executable
if system == "windows":
    mitm_path = "mitmdump.exe"
    with open(mitm_path, "wb") as file:
        z = zipfile.ZipFile(
            io.BytesIO(
                requests.get(
                    "https://snapshots.mitmproxy.org/9.0.1/mitmproxy-9.0.1-windows.zip"
                    ).content
                )
            )
        file.write(z.read(mitm_path))
        
elif system == "linux":
    mitm_path = "mitmdump"
    
    url = "https://snapshots.mitmproxy.org/9.0.1/mitmproxy-9.0.1-linux.tar.gz"    
    response = requests.get(url)
    content = io.BytesIO(response.content)

    with tarfile.open(fileobj=content, mode="r:gz") as tar:
        # Extract the "mitmbump" file to "myfolder"
        if mitm_path in tar.getnames():
            member = tar.getmember(mitm_path)
            with tar.extractfile(member) as f:
                with open(mitm_path, "wb") as outfile:
                    outfile.write(f.read())
    
    os.system(f"chmod -x {mitm_path}")


else:
    raise NotImplementedError(f"{system} is not supported")
