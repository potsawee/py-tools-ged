import os

try:
    import matplotlib.pyplot as plt
except:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

class SequenceLabelerTrainParser(object):
    def __init__(self):
        self.counter = 0
        self.logs = []
        self.names = []

    def read(self, path):
        with open(path, 'r') as file:
            log = file.read()
        log_dict = dict()
        for line in log.splitlines():
            try:
                feature, _value = line.split(': ')
            except ValueError: # incomplete file
                continue
            try:
                value = float(_value)
            except ValueError: # feature containing text
                continue
            if feature in log_dict:
                log_dict[feature].append(value)
            else:
                log_dict[feature] = [value]

        self.counter += 1
        self.names.append(os.path.basename(path))
        self.logs.append(log_dict)

    def list_features(self):
        if self.counter > 0:
            print(self.logs[0].keys())
        else:
            print("Read a log file first")

    def compare_models(self, feature, savepath=None):
        max_epoch = 20
        x = range(1,max_epoch+1)
        for log, name in zip(self.logs, self.names):
            y = log[feature]
            plt.plot(x, y, label=name)
        plt.legend()
        plt.ylabel(feature)
        plt.xlabel('epoch')
        if savepath == None:
            plt.show()
        else:
            plt.savefig(savepath)
