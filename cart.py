def fill(
    template, # name of template file name
    data, # dictionary of values where keys correspond to ids in the svg template
    data_type = "div", # "div"ering or "seq"uential data
    bands = 5, # for seq data; number of bands
    based = True, # for seq data; if data has a baseline value
    threshold = None, # list of threshold values
    colour = None, # list of colours to use
    area_keyword = 'path id', # keyword used to identify area paths
    replace_string = 'id="{}"' # string to replace, with format placeholder
):
    import statistics, math
    values = []
    for area in data:
        values.append(abs(data[area]))
    mean = statistics.mean(values)
    if data_type == "seq":
        if bands < 5 or bands > 7:
            print("Number of bands must be between 5 and 7")
            quit()
        if colour == None:
            if bands == 5:
                colour = ['#fef0d9','#fdcc8a','#fc8d59','#e34a33','#b30000']
            elif bands == 6:
                colour = ['#fef0d9','#fdd49e','#fdbb84','#fc8d59','#e34a33','#b30000']
            elif bands == 7:
                colour = ['#fef0d9','#fdd49e','#fdbb84','#fc8d59','#ef6548','#d7301f','#990000']
        if based == True:
            q = statistics.quantiles(values, n = 100, method = "inclusive")
        else:
            q = [0]
        mean_index = ((bands + 1) // 2)
        step = math.sqrt(mean - q[0]) / mean_index
        if threshold == None:
            threshold = []
            for i in range(bands):
                threshold.append(math.pow(i * step, 2) + q[0])
    else:
        if colour == None:
            colour = ['#8c510a','#d8b365','#f6e8c3','#c7eae5','#5ab4ac','#01665e']
        if threshold == None:
            threshold = [-999, -mean, -mean / 4, 0, mean / 4, mean]
    print("Thresholds:", ["{:.0f}".format(i) for i in threshold])
    with open(template + ".svg", newline = "", encoding = "utf-8") as file_in:
        with open(template + "-result.svg", "w", newline = "", encoding = "utf-8") as file_out:
            for row in file_in:
                if row.find(area_keyword) > -1:
                    for k, v in data.items():
                        if row.find(k) > -1:
                            i = 0
                            while i < bands - 1:
                                if v >= threshold[i + 1]:
                                    i += 1
                                else:
                                    break
                            file_out.write(row.replace(replace_string.format(k), 'fill="{}"'.format(colour[i])))
                            break
                else:
                    file_out.write(row)
