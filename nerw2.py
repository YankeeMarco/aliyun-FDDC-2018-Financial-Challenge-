import pycrfsuite
import  re,os
import time

# time.sleep(8000)
def data_generator_x():
    for  i in  os.listdir('/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/'):
        x,y =  tokenit('/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/'+i)
        yield x
def data_generator_y():
    for  i in  os.listdir('/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/'):
        x,y = tokenit('/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/'+i)
        yield y
def tokenit(path1):
    with open(path1,'r') as rf:
        strr = rf.read()
        list_x_y = re.split(r'[\n\t]', strr)
        x_train = list_x_y[0::2]
        y_train = list_x_y[1::2]
    return x_train[:-1], y_train

trainer = pycrfsuite.Trainer(verbose=True)
x = data_generator_x()
y = data_generator_y()
for i in range(2770):
    trainer.append(next(x), next(y))

 # Submit training data to the trainer
# for xseq, yseq in zip(x_train, y_train):
#     print("hh")
#     trainer.append(xseq, yseq)

# Set the parameters of the model
trainer.set_params({
    # coefficient for L1 penalty
    'c1': 0.1,

    # coefficient for L2 penalty
    'c2': 0.01,

    # maximum number of iterations
    'max_iterations': 200,

    # whether to include transitions that
    # are possible, but not observed
    'feature.possible_transitions': True
})

# Provide a file name as a parameter to the train function, such that
# the model will be saved to the file when training is finished
trainer.train('/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/crf.model')