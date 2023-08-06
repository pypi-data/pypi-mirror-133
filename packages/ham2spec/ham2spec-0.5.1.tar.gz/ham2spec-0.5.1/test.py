import numpy as np
import ham2spec
from time import perf_counter
from dataclasses import dataclass
from pathlib import Path


DEFAULT_CONFIG = {
    "xfrom": 11790,
    "xto": 13300,
    "xstep": 1,
    "bandwidth": 70,
    "shift_diag": -2420,
    "dip_cor": 0.014,
    "delete_pig": 0,
    "use_shift_T": False,
    "scale": False,
    "overwrite": False,
    "save_figs": False,
    "save_intermediate": False,
    "empirical": False,
    "normalize": False
}


@dataclass(frozen=True)
class Config:
    xfrom: int
    xto: int
    xstep: int
    bandwidth: float
    shift_diag: float
    dip_cor: float
    delete_pig: int
    use_shift_T: bool
    scale: bool
    overwrite: bool
    save_figs: bool
    save_intermediate: bool
    empirical: bool
    normalize: bool

def main():
    validation_data_dir = Path.cwd() / "validation_data"
    ham = np.loadtxt(validation_data_dir / "hamiltonian.txt", delimiter=",", dtype=np.float64).reshape((7,7))
    mus_single = np.loadtxt(validation_data_dir / "dipole_moments.txt", dtype=np.float64).reshape((7,3))
    rs_single = np.loadtxt(validation_data_dir / "positions.txt", dtype=np.float64).reshape((7,3))
    config_opts = DEFAULT_CONFIG.copy()
    config_opts["bandwidth"] = 120
    config = Config(**config_opts)
    hams = np.empty((100, 7, 7))
    mus = np.empty((100, 7, 3))
    rs = np.empty((100, 7, 3))
    for i in range(100):
        hams[i] = ham
        mus[i] = mus_single
        rs[i] = rs_single
    # sticks = ham2spec.compute_stick_spectra(hams, mus, rs)
    # a_stick = sticks[0]
    # _ = a_stick["e_vals"]
    # _ = a_stick["e_vecs"]
    # _ = a_stick["stick_abs"]
    # _ = a_stick["stick_cd"]
    # _ = a_stick["exciton_mus"]
    # broadened = ham2spec.compute_broadened_spectra(hams, mus, rs, config)
    # _ = broadened["x"]
    # _ = broadened["abs"]
    # _ = broadened["cd"]
    n = 1_000
    times = list()
    for _ in range(n):
        t_start = perf_counter()
        broadened = ham2spec.compute_broadened_spectra(hams, mus, rs, config)
        t_stop = perf_counter()
        times.append(t_stop - t_start)
    per_call = sum(times) / n * 1e6
    print(f"{per_call:.3f}us per call")


if __name__ == "__main__":
    main()