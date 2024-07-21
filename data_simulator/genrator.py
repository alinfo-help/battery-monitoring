# import csv
# import time
# import random
# from datetime import datetime

# def generate_data():
#     fieldnames = ["DateTime"] + [f"Bank1.B{i+1}" for i in range(19)] + ["Temperature", "Current"]
#     filename = '../data/battery_data.csv'

#     with open(filename, mode='w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
        
#         while True:
#             row = {
#                 "DateTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#                 "Temperature": round(random.uniform(35.0, 40.0), 1),
#                 "Current": round(random.uniform(5.0, 10.0), 2)
#             }
#             for i in range(19):
#                 row[f"Bank1.B{i+1}"] = round(random.uniform(6.0, 8.0), 3)
            
#             writer.writerow(row)
#             file.flush()
#             time.sleep(5)

# if __name__ == "__main__":
#     generate_data()

########################################################################################################################################
import csv
import time
import random
from datetime import datetime

def generate_data():
    fieldnames = ["DateTime"] + [f"Bank1.B{i+1}" for i in range(56)] + ["Temperature", "Current"]
    filename = '../data/battery_data.csv'

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        while True:
            row = {
                "DateTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "Temperature": round(random.uniform(35.0, 40.0), 1),
                "Current": round(random.uniform(5.0, 10.0), 2)
            }
            for i in range(56):
                row[f"Bank1.B{i+1}"] = round(random.uniform(6.0, 8.0), 3)
            
            writer.writerow(row)
            file.flush()
            
            # Log the newly written data
            print(f"Generated Data at {row['DateTime']}:")
            # for key, value in row.items():
            #     if key != "DateTime":
            #         print(f"  {key}: {value}")
            print("Data written to CSV file.\n")
            
            time.sleep(5)

if __name__ == "__main__":
    generate_data()

