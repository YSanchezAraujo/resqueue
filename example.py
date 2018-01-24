import numpy as np

# iteration variables
N_sub = 25
N_jobs = 500
effect = "effect"
seeds = (np.arange(0, 500)+1).astype(int)
starts = np.arange(0, 500, 5)
ends = np.arange(5, 505, 5)
seed_groups = [seeds[start:end] for start, end in zip(starts, ends)]

submit_dir = "/jukebox/daw/yoel/rstan_simulations/submit_dir"

# formatting sequence should be: nsub, effect, nsub, seed
data_dir = "/jukebox/daw/yoel/rstan_simulations/input_data"
data_fmt = "{}sub/2step/{}/data-nsub-{}-seed-{}.csv"
data_path = os.path.join(data_dir, data_fmt)
covar_fmt = "{}/sub/2step/{}/data_covar-nsub-{}-seed-{}.csv"
covar_path = os.path.join(data_dir, covar_fmt)

def fmt_groups(fmt_str, groups, nsub, eff):
    return [[fmt_str.format(nsub, eff, nsub, seed)
            for seed in group] for group in groups]

data_fmt_groups = fmt_groups(data_path, seed_groups, N_sub, effect)
covar_fmt_groups = fmt_groups(covar_path, seed_groups, N_sub, effect)

resources = {"mem":4, "cores":4, "time":"2-23:00:00"}
d0 = reformat_input(data_fmt_groups[0])
c0 = reformat_input(covar_fmt_groups[0])
call_items = {"script": "~/Desktop/yoel/run_script.R", "data_files":d0, "covar_files":c0}
print(make_call_cmd(call_items, resources, "R"))
