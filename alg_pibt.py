from alg_pibt_funcitons import *
from run_single_MAPF_func import run_mapf_alg


def run_procedure_pibt(
        agent_i: AgentAlg,
        agent_j: AgentAlg | None,
        config_from: Dict[str, Node],
        config_to: Dict[str, Node],
        agents_dict: Dict[str, AgentAlg],
        nodes_dict: Dict[str, Node],
        h_dict: Dict[str, np.ndarray],
        blocked_nodes: List[Node],
) -> bool:  # valid or invalid

    nei_nodes = get_sorted_nei_nodes(agent_i, config_from, nodes_dict, h_dict)

    for j, nei_node in enumerate(nei_nodes):
        if there_is_vc(nei_node, config_to):
            continue
        if agent_j is not None and config_from[agent_j.name] == nei_node:
            continue
        if nei_node in blocked_nodes:
            continue
        config_to[agent_i.name] = nei_node
        agent_k = get_agent_k(nei_node, config_from, config_to, agents_dict)
        if agent_k is not None:
            valid = run_procedure_pibt(
                agent_k, agent_i, config_from, config_to, agents_dict, nodes_dict, h_dict, blocked_nodes
            )
            if not valid:
                continue
        return True
    config_to[agent_i.name] = config_from[agent_i.name]
    return False



def run_pibt(
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
    agents: List[AgentAlg] = []
    agents_dict: Dict[str, AgentAlg] = {}
    for num, (s_node, g_node) in enumerate(zip(start_nodes, goal_nodes)):
        new_agent = AgentAlg(num, s_node, g_node)
        agents.append(new_agent)
        agents_dict[new_agent.name] = new_agent
    agents.sort(key=lambda a: a.priority, reverse=True)

    iteration = 0
    finished = False
    while not finished:

        config_from: Dict[str, Node] = {a.name: a.path[-1] for a in agents}
        config_to: Dict[str, Node] = {}

        # calc the step
        for agent in agents:
            if agent.name not in config_to:
                _ = run_procedure_pibt(agent, None, config_from, config_to, agents_dict, nodes_dict, h_dict, [])

        # execute the step + check the termination condition
        finished = True
        agents_finished = []
        for agent in agents:
            next_node = config_to[agent.name]
            agent.path.append(next_node)
            agent.prev_node = agent.curr_node
            agent.curr_node = next_node
            if agent.curr_node != agent.goal_node:
                finished = False
                agent.priority += 1
            else:
                agent.priority = agent.init_priority
                agents_finished.append(agent)

        # unfinished first
        agents.sort(key=lambda a: a.priority, reverse=True)

        # print + render
        runtime = time.time() - start_time
        print(f'\r{'*' * 10} | [PIBT] {iteration=: <3} | finished: {len(agents_finished)}/{len(agents): <3} | runtime: {runtime: .2f} seconds | {'*' * 10}', end='')
        iteration += 1

        if runtime > max_time:
            return None, {}

    # checks
    for i in range(len(agents[0].path)):
        check_vc_ec_neic_iter(agents, i, to_count=False)

    return {a.name: a.path for a in agents}, {'agents': agents}


@use_profiler(save_dir='stats/alg_pibt.pstat')
def main():
    params = {'max_time': 100}
    run_mapf_alg(alg=run_pibt, params=params)


if __name__ == '__main__':
    main()

