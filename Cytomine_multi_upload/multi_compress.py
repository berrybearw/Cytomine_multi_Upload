import os
import shutil
from pathlib import Path
import logging

def pack_mrxs_related_files(base_dir_path):
    base_dir = Path(base_dir_path)
    zip_output_dir = base_dir / "zip"
    zip_output_dir.mkdir(exist_ok=True)

    # Set up log file
    log_file = base_dir / "pack_mrxs.log"
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )

    logging.info("Started packing MRXS related files")

    # Search for all .mrxs files
    mrxs_files = list(base_dir.glob("*.mrxs"))

    for mrxs_file in mrxs_files:
        try:
            base_name = mrxs_file.stem
            xml_file = base_dir / f"{base_name}.xml"
            folder = base_dir / base_name

            # 建立一個暫存資料夾來放所有要壓縮的內容
            temp_dir = base_dir / f"__temp_{base_name}"
            temp_dir.mkdir(exist_ok=True)

            # 複製 mrxs 檔案
            shutil.copy(mrxs_file, temp_dir / mrxs_file.name)
            logging.info(f"Copied: {mrxs_file.name}")

            # 複製 xml（如果有）
            if xml_file.exists():
                shutil.copy(xml_file, temp_dir / xml_file.name)
                logging.info(f"Copied: {xml_file.name}")

            # 複製資料夾（如果有）
            if folder.exists() and folder.is_dir():
                shutil.copytree(folder, temp_dir / folder.name)
                logging.info(f"Copied folder: {folder.name}")

            # 壓縮
            zip_output = zip_output_dir / base_name
            archive_path = shutil.make_archive(str(zip_output), 'zip', root_dir=temp_dir)
            logging.info(f"Created zip: {archive_path}")
            print(f"Created zip: {archive_path}")

            # 刪除暫存資料夾
            shutil.rmtree(temp_dir)

        except Exception as e:
            logging.error(f"Error processing {mrxs_file.name}: {str(e)}")
            print(f"Error processing {mrxs_file.name}: {str(e)}")

if __name__ == "__main__":
    pack_mrxs_related_files(".")