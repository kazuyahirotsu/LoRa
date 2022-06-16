with open("./6_16_processed.log", mode='w') as new:
    with open('./rangetest_results/rangetest6_16.log') as f:
        for line in f:
            if ("chan" not in line) and ("N," in line):
                rssi_start_index = line.find("RSSI")+5
                rssi_stop_index = line.find("dBm")
                rssi = line[rssi_start_index:rssi_stop_index]

                lat_start_index = line.find(",",line.find("message"))
                lat_stop_index = line.find(",",lat_start_index+1)
                lat = line[lat_start_index:lat_stop_index]

                lon_start_index = line.find(",",line.find("N"))
                lon_stop_index = line.find(",",lon_start_index+1)
                lon = line[lon_start_index:lon_stop_index]               
                new.write(rssi+lat+lon)
                new.write("\n")