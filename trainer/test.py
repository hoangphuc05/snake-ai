from trainer_function import CustomTrainer
import os
os.environ['CUDA_VISIBLE_DEVICES'] = "1"
trainer = CustomTrainer()
# trainer.train('bot-2.csv', 'train_model/sigmoid-8-8-bot2.h5','sigmoid','sigmoid', [[8, 'sigmoid'], [8, 'sigmoid']])

print(trainer.run_evaluation('train_model/sigmoid-8-8-bot2.h5'))