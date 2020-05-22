def fill(
    template, # name of template file name
    data, # dictionary of values where keys correspond to ids in the svg template
    data_type = "div", # "div"ering or "seq"uential data
    bands = 5, # for seq data; number of bands
    based = True, # for seq data; if data has a baseline value
    threshold = None, # list of threshold values
    colour = None, # list of colours to use
    area_keyword = 'Z" id', # keyword used to identify area paths
    replace_string = 'id="{}"' # string to replace, with format placeholder
):
    import statistics, math
    if threshold == None:
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
                    colour = ['#feebe2','#fbb4b9','#f768a1','#c51b8a','#7a0177']
                elif bands == 6:
                    colour = ['#feebe2','#fcc5c0','#fa9fb5','#f768a1','#c51b8a','#7a0177']
                elif bands == 7:
                    colour = ['#feebe2','#fcc5c0','#fa9fb5','#f768a1','#dd3497','#ae017e','#7a0177']
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
            bands = 6
            if colour == None:
                colour = ['#8c510a','#d8b365','#f6e8c3','#c7eae5','#5ab4ac','#01665e']
            if threshold == None:
                threshold = [0, -mean, -mean / 4, 0, mean / 4, mean]
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
    if bands == 6:
        print("|" + colour[5] + "|" + " lead > " + "{:,.0f}".format(round(abs(threshold[5]) / 100) * 100))
        print("|" + colour[4] + "|" + " lead > " + "{:,.0f}".format(round(abs(threshold[4]) / 100) * 100))
        print("|" + colour[3] + "|" + " lead < " + "{:,.0f}".format(round(abs(threshold[4]) / 100) * 100))
        print("|" + colour[2] + "|" + " lead < " + "{:,.0f}".format(round(abs(threshold[2]) / 100) * 100))
        print("|" + colour[1] + "|" + " lead > " + "{:,.0f}".format(round(abs(threshold[2]) / 100) * 100))
        print("|" + colour[0] + "|" + " lead > " + "{:,.0f}".format(round(abs(threshold[1]) / 100) * 100))
