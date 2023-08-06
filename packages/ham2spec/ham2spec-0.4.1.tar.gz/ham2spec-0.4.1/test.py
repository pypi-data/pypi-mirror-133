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
    ham = np.loadtxt("ham.txt", delimiter=",", dtype=np.float64)
    mus = np.loadtxt("pig_mus.txt", dtype=np.float64)
    pos = np.loadtxt("pig_pos.txt", dtype=np.float64)
    stick = ham2spec.compute_stick_spectrum(ham, mus, pos)
    config_opts = DEFAULT_CONFIG.copy()
    config_opts["bandwidth"] = 120
    config = Config(**config_opts)
    broadened = ham2spec.compute_broadened_spectrum_from_stick(stick, config)
    output_dir = Path.cwd() / "test_output"
    output_dir.mkdir(exist_ok=True)
    outdata = np.empty((len(broadened["x"]), 2))
    outdata[:, 0] = broadened["x"]
    outdata[:, 1] = broadened["abs"]
    np.savetxt(output_dir / "abs.txt", outdata, delimiter=",")
    outdata[:, 1] = broadened["cd"]
    np.savetxt(output_dir / "cd.txt", outdata, delimiter=",")
    # n = 100_000
    # times = list()
    # for _ in range(n):
    #     t_start = perf_counter()
    #     _ = ham2spec.compute_stick_spectrum(ham, mus, pos)
    #     t_stop = perf_counter()
    #     times.append(t_stop - t_start)
    # per_call = sum(times) / n * 1e6
    # print(f"{per_call:.3f}us per call")


if __name__ == "__main__":
    main()