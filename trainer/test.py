from trainer_function import CustomTrainer


### 4 layer activation function Neural Network!!!

# layer1 = 16
# layer2 = 32
# layer3 = 64 
# layer4 = 16
# l1Activation = ['relu','relu','elu','elu','sigmoid','sigmoid','sigmoid','relu','sigmoid','sigmoid','sigmoid','elu','relu','relu','relu','elu','relu','relu','relu','sigmoid']
# l2Activation = ['elu','relu','relu','elu','relu','sigmoid','sigmoid','sigmoid','elu','sigmoid','sigmoid','sigmoid','elu','relu','relu','relu','sigmoid','relu','relu','relu']
# l3Activation = ['relu','elu','relu','relu','sigmoid','relu','sigmoid','sigmoid','sigmoid','elu','sigmoid','sigmoid','relu','elu','relu','relu','relu','sigmoid','relu','relu']
# l4Activation = ['elu','elu','elu','relu','sigmoid','sigmoid','relu','sigmoid','sigmoid','sigmoid','elu','sigmoid','relu','relu','elu','relu','relu','relu','sigmoid','relu']
# fileSave = ['rere-16-32-64-16-bot2.h5', 'rree-16-32-64-16-bot2.h5', 'erre-16-32-64-16-bot2.h5', 'eerr-16-32-64-16-bot2.h5', 
#             'srss-16-32-64-16-bot2.h5', 'ssrs-16-32-64-16-bot2.h5', 'sssr-16-32-64-16-bot2.h5', 'rsss-16-32-64-16-bot2.h5', 
#             'sess-16-32-64-16-bot2.h5', 'sses-16-32-64-16-bot2.h5', 'ssse-16-32-64-16-bot2.h5', 'esss-16-32-64-16-bot2.h5', 
#             'rerr-16-32-64-16-bot2.h5', 'rrer-16-32-64-16-bot2.h5', 'rrre-16-32-64-16-bot2.h5', 'errr-16-32-64-16-bot2.h5', 
#             'rsrr-16-32-64-16-bot2.h5', 'rrsr-16-32-64-16-bot2.h5', 'rrrs-16-32-64-16-bot2.h5', 'srrr-16-32-64-16-bot2.h5', 
#             ]

# f = open("./trainer/report.txt", 'a')
# trainer = CustomTrainer()
# for i in range(len(fileSave)):
#     f = open("./trainer/report.txt", 'a')
#     f.writelines('Running Analysis for 4 layers w/ following layers and activation functions: \n')
#     f.writelines('Layers: ' + str(layer1)+ ' ' + str(layer2)+ ' ' + str(layer3)+ ' ' + str(layer4) + '\n')
#     f.writelines('Activation: ' + str(l1Activation[i])+ ', ' + str(l2Activation[i])+ ', ' + str(l3Activation[i])+ ', ' + str(l4Activation[i]) + '\n')
#     layers = '[[' + str(layer1) + ',' + l1Activation[i]+ '], ['+str(layer2)+','+l2Activation[i]+'] , [' +str(layer3)+','+l3Activation[i]+'], [' +str(layer4)+','+l4Activation[i]+']]'
#     f.write(layers + '\n')
#     trainer.train('bot-2.csv', fileSave[i], 'sigmoid', 'sigmoid', [[layer1, l1Activation[i]], [layer2, l2Activation[i]], [layer3, l3Activation[i]] , [layer4, l4Activation[i]]])
#     avgScore = trainer.run_evaluation(fileSave[i])
#     avgAccuracy = trainer.getAverageAccuracy()
#     f.write('Average Score: ' + str(avgScore) + ' | Average Accuracy: ' + str(avgAccuracy) + '\n')
#     f.write('Output as file: ' + fileSave[i]+'\n')
#     f.write('-------------------------------------------------------------------- \n \n')
#     f.close()
# f.close()

## 2 layer Activation function Neural Network!!!
layer1 = 16
layer2 = 8
l1Activation = ['relu','sigmoid','elu','sigmoid','softmax','relu','elu','softmax','relu','softmax','elu']
l2Activation = ['sigmoid','elu','sigmoid','softmax','sigmoid','elu','relu','relu','softmax','elu','softmax']
fileSave = ['rs-16-8-bot2.h5', 'se-16-8-bot2.h5', 'es-16-8-bot2.h5',
            'ssmx-16-8-bot2.h5', 'smxs-16-8-bot2.h5', 're-16-8-bot2.h5', 'er-16-8-bot2.h5',
            'smxr-16-8-bot2.h5', 'rsmx-16-8-bot2.h5', 'smxe-16-8-bot2.h5', 'esmx-16-8-bot2.h5',
            ]

trainer = CustomTrainer()
for i in range(len(fileSave)):
    f = open("./trainer/report.txt", 'a')
    f.writelines('Running Analysis for 2 layers w/ following layers and activation functions: \n')
    f.writelines('Layers: ' + str(layer1)+ ' ' + str(layer2)+ '\n')
    f.writelines('Activation: ' + str(l1Activation[i])+ ', ' + str(l2Activation[i]) + '\n')
    layers = '[[' + str(layer1) + ',' + l1Activation[i]+ '], ['+str(layer2)+','+l2Activation[i]+']]'
    f.write(layers + '\n')
    trainer.train('bot-2.csv', fileSave[i], 'sigmoid', 'sigmoid', [[layer1, l1Activation[i]], [layer2, l2Activation[i]]])
    avgScore = trainer.run_evaluation(fileSave[i])
    avgAccuracy = trainer.getAverageAccuracy()
    f.write('Average Score: ' + str(avgScore) + ' | Average Accuracy: ' + str(avgAccuracy) + '\n')
    f.write('Output as file: ' + fileSave[i]+'\n')
    f.write('-------------------------------------------------------------------- \n \n')
    f.close()
