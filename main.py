# Python 2 code, compatible with Python 3
import urllib.request
import os
import shutil


def download(url, file_path, timeout=10):

    if os.path.exists(file_path):
        print("File \"" + file_path.split("/").pop() + "\" already existed!")
        if input('Do you want to delete and re-download it [Y/N]? ').lower() != 'y':
            print("The program is exiting according to your instruction. ")
            return
        else:
            os.remove(file_path)

    block_size = 1024 * 100  # 1kb
    tmp_file_path = file_path + ".part"

    # tmp file
    print("\nRemote URL: " + str(url))
    first_byte = os.path.getsize(tmp_file_path) if os.path.exists(tmp_file_path) else 0
    print("Downloading with urllib from Byte " + str(first_byte))

    file_size = -1

    try:
        file_size = int(urllib.request.urlopen(url).info().get("Content-Length", -1))
        print("File size: " + str(file_size) + "\n")

        while first_byte < file_size:
            try:
                if first_byte + block_size - 1 >= file_size:
                    last_byte = file_size
                else:
                    last_byte = first_byte + block_size - 1

                print("Downloading from Byte " + str(first_byte) + " to Byte " + str(last_byte) + '... ', end='')
                headers = {
                    "Range": "bytes=%s-%s" % (first_byte, last_byte),
                    "Group": 1
                }
                req = urllib.request.Request(url, headers=headers)
                page = urllib.request.urlopen(req, timeout=timeout).read()
                print("OK")

                with open(tmp_file_path, "ab") as f:
                    f.write(page)
                first_byte = last_byte + 1
            except Exception as e:
                print("Caught Error" + str(e))
                print("Retry...")

    except Exception as e:
        print(e)
    finally:
        # rename the temp download file to the correct name if fully downloaded
        if file_size == os.path.getsize(tmp_file_path):
            shutil.move(tmp_file_path, file_path)
            print("\nCompleted. ")
        elif file_size == -1:
            raise Exception("Error getting Content-Length from server: %s" % url)

    return


print("Resumable HTTP Downloader\nGroup 1, COMP2322, PolyU\n")
download("http://158.132.255.107:25003/project/team1.txt", "./team1.txt")