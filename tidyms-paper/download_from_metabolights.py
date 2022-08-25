from ftplib import FTP
import os
import pandas as pd


def start_ftp():
    sample_path = \
        "pub/databases/metabolights/studies/public/MTBLS1919/Applications"
    ftp = FTP("ftp.ebi.ac.uk")
    ftp.login()
    ftp.cwd(sample_path)
    return ftp


def make_dir_safe(path="data"):
    if os.path.exists(path):
        print("{} directory found. Checking files...".format(path))
    else:
        print("{} directory doesn't exist. Creating directory...".format(path))
        os.makedirs(path)


def download_file_ftp(ftp, fname, download_dir="data"):
    fname_path = os.path.join(download_dir, fname)
    exists_sample_list = os.path.exists(fname_path)
    if exists_sample_list:
        msg = "{} found".format(fname)
        print(msg)
    else:
        msg = "{} missing. Downloading from Metabolights...".format(fname)
        print(msg)
        with open(fname_path, "wb") as fin:
            ftp.retrbinary("RETR " + fname, fin.write)


def download_centroid_data(ftp, download_dir="data"):
    sample_list_path = os.path.join(download_dir, "sample_list.csv")
    sample_list = pd.read_csv(sample_list_path)
    centroid_filenames = sample_list["id"] + ".mzML"
    centroid_data_path = [os.path.join(download_dir, "cent", x) for x in
                          centroid_filenames]
    sample_list["sample_path"] = centroid_data_path
    exists_centroid_data = all(os.path.exists(x) for x in centroid_data_path)
    if exists_centroid_data:
        print("Centroid data found.")
    else:
        print("Centroid data missing. Downloading from Metabolights...")
        centroid_data_path = os.path.join(download_dir, "cent")
        make_dir_safe(centroid_data_path)
        centroid_data_ftp_dir = "Centroid_data"
        for filename in centroid_filenames:
            file_ftp_path = os.path.join(centroid_data_ftp_dir, filename)
            file_path = os.path.join(centroid_data_path, filename)
            with open(file_path, "wb") as fin:
                print("Downloading {} into {}".format(filename,
                                                      centroid_data_path))
                ftp.retrbinary("RETR " + file_ftp_path, fin.write)


def get_application1_data(download_dir):
    ftp = start_ftp()
    make_dir_safe(download_dir)
    download_file_ftp(ftp, "sample_list.csv", download_dir=download_dir)
    download_centroid_data(ftp, download_dir=download_dir)
    ftp.close()
    

def get_application2_data(download_dir):
    ftp = start_ftp()
    make_dir_safe(download_dir)
    download_file_ftp(ftp, "NIST001.csv", download_dir=download_dir)
    download_file_ftp(ftp, "run-order-data.csv", download_dir=download_dir)
    ftp.close()
