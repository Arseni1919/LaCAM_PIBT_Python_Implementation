from alg_pibt_funcitons import *
from run_single_MAPF_func import run_mapf_alg


def run_pibt(
        start_nodes: List[Node],
        goal_nodes: List[Node],
        nodes: List[Node],
        nodes_dict: Dict[str, Node],
        h_dict: Dict[str, np.ndarray],
        map_dim: Tuple[int, int],
        params: Dict
) -> None | Tuple[Dict[str, List[Node]], Dict]:
    pass


@use_profiler(save_dir='stats/alg_pibt.pstat')
def main():
    params = {}
    run_mapf_alg(alg=run_pibt, params=params)


if __name__ == '__main__':
    main()

