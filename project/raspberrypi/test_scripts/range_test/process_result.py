with open("./rangetest_results/compare_6_16_processed_and_ID.log", mode='w') as new:
    with open('./rangetest_results/rangetest6_16.log') as f:
        count = 0
        before_count = 0
        for line in f:
            if ("chan" not in line) and ("N," in line):

                rssi_start_index = line.find("RSSI")+5
                rssi_stop_index = line.find("dBm")
                rssi = line[rssi_start_index:rssi_stop_index]

                id_start_index = line.find("=",line.find("message"))+1
                id_stop_index = line.find(",",id_start_index+1)+1
                id = line[id_start_index:id_stop_index]
                try:
                    count = int(line[id_start_index:id_stop_index-1])
                    if count != before_count+1:
                        new.write("\n")
                    before_count = count
                except:
                    print(Exception)


                lat_start_index = line.find(",",line.find("message"))
                lat_stop_index = line.find(",",lat_start_index+1)
                lat = line[lat_start_index:lat_stop_index]

                lon_start_index = line.find(",",line.find("N"))
                lon_stop_index = line.find(",",lon_start_index+1)
                lon = line[lon_start_index:lon_stop_index]               
                new.write(id+rssi+lat+lon)
                new.write("\n")

# with open("./rangetest_results/compare_send_6_16_processed_and_ID.log", mode='w') as new:
#     with open('./rangetest_results/send6_16.log') as f:
#         for line in f:
#             if ("chan" not in line) and ("N," in line):

#                 id_start_index = line.find(" ",line.find(","))+1
#                 id_stop_index = line.find(",",id_start_index+1)+1
#                 id = line[id_start_index:id_stop_index]

#                 lat_start_index = id_stop_index
#                 lat_stop_index = line.find(",",lat_start_index+1)
#                 lat = line[lat_start_index:lat_stop_index]

#                 lon_start_index = line.find(",",line.find("N"))
#                 lon_stop_index = line.find(",",lon_start_index+1)
#                 lon = line[lon_start_index:lon_stop_index]               
#                 new.write(id+lat+lon)
#                 new.write("\n")