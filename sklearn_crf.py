import sklearn_crfsuite
import  re,os

def tokenit(path1):
    with open(path1,'r') as rf:
        strr = rf.read()
        list_x_y = re.split(r'[\n\t]', strr)
        x_train = list_x_y[0::2][:-1]
        y_train = list_x_y[1::2]
        return x_train, y_train
x_train = []
y_train =[]

for  i in  os.listdir('/home/47_7/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/')[0:3]:
    x,y =  tokenit('/home/47_7/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/'+i)
    if len(x)==len(y):
        x_train += x
        y_train += y
    if len(x_train)==len(y_train):
        print("It is OK {}".format(i))
    else:
        print("baaaaad")


crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)
crf.fit(x_train, y_train)