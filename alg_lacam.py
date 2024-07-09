import random

from alg_lacam_funcitons import *
from run_single_MAPF_func import run_mapf_alg


def run_procedure_pibt():
    pass


def run_lacam(
        start_nodes: List[Node],
        goal_nodes: List[Node],
        nodes: List[Node],
        nodes_dict: Dict[str, Node],
        h_dict: Dict[str, np.ndarray],
        map_dim: Tuple[int, int],
        params: Dict
) -> Tuple[None, Dict] | Tuple[Dict[str, List[Node]], Dict]:

    max_time = params['max_time']

    start_time = time.time()

    # create agents
    agents, agents_dict = create_agents(start_nodes, goal_nodes)
    n_agents = len(agents_dict)

    config_start: Dict[str, Node] = {a.name: a.start_node for a in agents}
    config_goal: Dict[str, Node] = {a.name: a.goal_node for a in agents}
    config_goal_name: str = get_config_name(config_goal)

    open_list: Deque[HighLevelNode] = deque()  # stack
    explored_dict: Dict[str, HighLevelNode] = {}   # stack
    init_order = get_init_order(agents, config_start, h_dict)
    N_init: HighLevelNode = HighLevelNode(config=config_start, tree=deque([get_C_init()]), order=init_order, parent=None)
    open_list.appendleft(N_init)
    explored_dict[N_init.name] = N_init

    iteration = 0
    while len(open_list) > 0:
        N: HighLevelNode = open_list[0]

        if N.name == config_goal_name:

            # checks
            # for i in range(len(agents[0].path)):
            #     check_vc_ec_neic_iter(agents, i, to_count=False)
            paths_dict = backtrack(N)
            for a_name, path in paths_dict.items():
                agents_dict[a_name].path = path
            return paths_dict, {'agents': agents}

        # low-level search end
        if len(N.tree) == 0:
            open_list.popleft()
            continue

        # low-level search
        C: LowLevelNode = N.tree.popleft()  # constraints
        if C.depth < n_agents:
            i_agent = N.order[C.depth]
            v = N.config[i_agent.name]
            neighbours = v.neighbours[:]
            random.shuffle(neighbours)
            for nei_name in neighbours:
                C_new = get_C_child(parent=C, who=i_agent, where=nodes_dict[nei_name])
                N.tree.append(C_new)

        config_new = get_new_config(N, C, agents_dict, nodes_dict, h_dict)
        if config_new is None:
            continue
        if get_config_name(config_new) in explored_dict:
            continue

        order, finished = get_order(config_new, N)
        N_new: HighLevelNode = HighLevelNode(config=config_new, tree=deque([get_C_init()]), order=order, parent=N, finished=finished)
        open_list.appendleft(N_new)
        explored_dict[N_new.name] = N_new

        # print + render
        runtime = time.time() - start_time
        print(
            f'\r{'*' * 10} | [PIBT] {iteration=: <3} | finished: {N_new.finished}/{n_agents: <3} | runtime: {runtime: .2f} seconds | {'*' * 10}',
            end='')
        iteration += 1

        if runtime > max_time:
            return None, {'agents': agents}

    return None, {'agents': agents}


@use_profiler(save_dir='stats/alg_lacam.pstat')
def main():
    params = {'max_time': 1000}
    run_mapf_alg(alg=run_lacam, params=params)


if __name__ == '__main__':
    main()
