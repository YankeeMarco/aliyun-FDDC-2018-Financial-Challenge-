import pycrfsuite
import  re,os
import time
from tokenization_entitylist_only import  tokenization_entis
import pickle

# time.sleep(8000)
# def data_generator_x():
#     for  i in  os.listdir('/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/'):
#         x,y =  tokenit('/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/'+i)
#         yield x
# def data_generator_y():
#     for  i in  os.listdir('/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/'):
#         x,y = tokenit('/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/'+i)
#         yield y

tnt = tokenization_entis()

def tokenit(path1):
    try:
        strr = tnt.tokenize_enti(path1)
        list_x_y = re.split(r'[\n\t]', strr)
        x_train = list_x_y[0::2][:-1]
        y_train = list_x_y[1::2]
        return x_train, y_train
    except Exception as e:
        print("sth wrong with the tokenization_entity_only")
        return [' '], ['o']

x_train = []
y_train =[]





if not os.path.exists('/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/xtrain.pkl'):
    for i in os.listdir('/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/'):
        x, y = tokenit('/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/' + i)
        if len(x) == len(y):
            x_train += x
            y_train += y
        if len(x_train) == len(y_train):
            print("It is OK {}".format(i))
        else:
            print("baaaaad")
    pickle.dump(x_train, open('/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/xtrain.pkl', 'wb'))
    pickle.dump(y_train, open('/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/ytrain.pkl', 'wb'))
else:
    x_train = pickle.load(open('/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/xtrain.pkl', 'rb'))
    y_train = pickle.load(open('/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/ytrain.pkl', 'rb'))

trainer = pycrfsuite.Trainer(verbose=True)
# x = data_generator_x()
# # y = data_generator_y()
# for i in range(700):
trainer.append(x_train, y_train)

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
print("start at {} longtime training.........".format(time.ctime()))
trainer.train('/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/crf.model')