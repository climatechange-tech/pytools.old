from auxiliary_functions import *

obs, sim = read_example_data()
plot_historgram(obs, sim, "tas_hist_original.png")
plot_qq(obs, sim, "tas_qq_original.png")