import model_utils as model_utils
import models as models
import torch


from StftData import StftData

from AudioDataUtils import *
import numpy as np


MODEL_DIR = "checkpoints/UNet_exp28/UNet_best_val.checkpoint"

combined = StftData(pickle_file = 'example_data/combined_1001.pkl')
biden = StftData(pickle_file='example_data/biden_1001.pkl')
trump = StftData(pickle_file='example_data/trump_1001.pkl')

container = StftData(pickle_file='example_data/combined_1001.pkl')

combined_np = combined.data
biden_np = biden.data
trump_np = trump.data
ideal_mask = np.ones_like(biden_np, dtype=np.float32) * (np.abs(biden_np) > np.abs(trump_np))




# # Play combined audio
# print("Playing combined audio")
# play(combined.invert())

# # First play the best case scenario mask.
# container.data = ideal_mask * combined_np
# print("playing best expected cleanup")
# play(container.invert())


# Model output:
print("Playing model output")
model = model_utils.load_model(models.get_model("UNet")(), MODEL_DIR).cpu()
model.eval()

# alpha = 0.85 # Higher removes more trump.
# x_input = torch.tensor(combined_np, requires_grad=False).cpu()
# x_input = torch.clamp_min(torch.log(x_input.abs()), 0)
# x_input = torch.reshape(x_input, (1, 1, 512, 128))
# pred = model(x_input).detach().numpy()
# pred_mask = np.ones_like(pred) * (pred > alpha)
# # pred_mask = pred
# # Could also consider multiplying in log space and then taking exp to get the result back
# container.data = pred_mask * combined_np
# play(container.invert())


alpha = 0.75 # Higher removes more trump.
x_input = torch.tensor(combined_np, requires_grad=False).cpu().abs()
# x_input = torch.clamp_min(torch.log(x_input.abs()), 0)
x_input = torch.reshape(x_input, (1, 1, 512, 128))
pred = model(x_input).detach().numpy()
pred_mask = np.ones_like(pred) * (pred > alpha)
# pred_mask = pred
container.data = pred_mask * combined_np
play(container.invert())


