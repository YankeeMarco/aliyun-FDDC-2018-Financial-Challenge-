

with open(r"/home/mm/Downloads/round1_train_20180518/hetong/hetong.train","r") as rfile:

    count=0
    while count<1000:
        line=rfile.readline()
        count+=1
        if len(line.split("\t"))==7:
            print("7, the row is {}".format(count))
        elif len(line.split("\t"))==8:
            print("8, the row is {}".format(count))
        else :
            print("aha {}, the row is {}".format(len(line.split("\t")),line))

