from nornir import InitNornir
from tqdm import tqdm
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
nr = InitNornir(config_file="config.yaml")


from tqdm import tqdm



def multiple_progress_bar(task, napalm_get_bar, other_bar):
    """
    This task takes two paramters that are in fact bars;
    napalm_get_bar and other_bar. When we want to tell
    to each respective bar that we are done and should update
    the progress we can do so with bar_name.update()
    """
    task.run(task=napalm_get, getters=["facts"])
    napalm_get_bar.update()
    tqdm.write(f"{task.host}: facts gathered")

    # more actions go here
    other_bar.update()
    tqdm.write(f"{task.host}: done!")


# we create the first bar named napalm_get_bar
with tqdm(
    total=len(nr.inventory.hosts), desc="gathering facts",
) as napalm_get_bar:
    # we create the second bar named other_bar
    with tqdm(
        total=len(nr.inventory.hosts), desc="other action   ",
    ) as other_bar:
        # we call our grouped task passing both bars
        nr.run(
            task=multiple_progress_bar,
            napalm_get_bar=napalm_get_bar,
            other_bar=other_bar,
        )
