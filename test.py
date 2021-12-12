# raw_ops = [{'op_type': 'w', 'var': 1, 'val': 1, 'client_id': 1, 'tra_id': 1}]
with open("output/result.txt") as in_file:
    raw_ops = in_file.readlines()

# print(raw_ops)

def run_oopsla_graph(raw_ops):
    causal_hist = OopslaAtomicHistoryPO(raw_ops)
    wr = causal_hist.get_wr()
    causal_hist.vis_includes(wr)
    causal_hist.vis_is_trans()
    # if causal_hist.check_read_zero():
    #     print('Read zero!')
    ww = causal_hist.casual_ww()
    for key, ww_x in ww.items():
        causal_hist.vis_includes(ww_x)
    causal_hist.vis_is_trans()
    if causal_hist.vis.has_cycle():
        print('BP1/4!!!!')