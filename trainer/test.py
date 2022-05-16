from trainer_function import CustomTrainer

trainer = CustomTrainer()
# trainer.train('bot-2.csv', 'elu-16-32-64-16-bot2.h5', [[16, 'sigmoid'], [32, 'sigmoid'], [64, 'sigmoid'] , [16, 'sigmoid']])

print(trainer.run_evaluation('elu-16-32-64-16-bot2.h5'))