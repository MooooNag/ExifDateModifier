import piexif
import os
from PIL import Image
from datetime import datetime, timedelta

keys_ts_taken = ["Exif", 36867, 36868]

directory_old_ts = "new"
directory_new_ts = "new_ts"
hours_offset = 1-48
minutes_offset = 0

for filename in os.listdir(directory_old_ts):
    f = os.path.join(directory_old_ts, filename)
    if os.path.isfile(f):
        print(f)
        img = Image.open(f)
        exif_dict = piexif.load(img.info['exif'])

        timestamp_string = str(exif_dict[keys_ts_taken[0]][keys_ts_taken[1]]).replace("b", "").replace("'", "")

        format = '%Y:%m:%d %H:%M:%S'
        datetime_object = datetime.strptime(timestamp_string, format)
        datetime_object = datetime_object + timedelta(hours=hours_offset, minutes=minutes_offset)
        timestamp_string = datetime_object.strftime(format);


        timestamp_bytes = bytes(timestamp_string, 'utf-8')

        exif_dict[keys_ts_taken[0]][keys_ts_taken[1]] = timestamp_bytes
        exif_dict[keys_ts_taken[0]][keys_ts_taken[2]] = timestamp_bytes

        exif_bytes = piexif.dump(exif_dict)
        img.save(os.path.join(directory_new_ts, filename), quality='keep', exif=exif_bytes)
