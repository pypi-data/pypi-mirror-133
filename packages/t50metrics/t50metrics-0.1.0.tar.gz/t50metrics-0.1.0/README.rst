Surgical Action Triplet Evaluation Metrics
------------------------------------------
Recognition Performance

# install
pip install t50metrics


# import
import t50metrics

# instantiate
num_tool = 6
num_verb = 10
num_target = 15
num_triplet = 100

mAP_i = t50metrics.Recognition(num_tool)
mAP_v = t50metrics.Recognition(num_verb)
mAP_t = t50metrics.Recognition(num_target)
mAP_ivt = t50metrics.Recognition(num_triplet)


mAP_i.reset()
mAP_v.reset()
mAP_t.reset()
mAP_ivt.reset()


mAP_i.update(target, predition)
mAP_ivt.update(target, prediction)

mAP_ivt.compute_AP()

mAP_ivt.video_end()

mAP_ivt.compute_video_AP()


mAP_ivt.compute_global_AP()


mAP_ivt.reset_video()

mAP_ivt.reset_global()


mAP_ivt.compute_per_video_mAP()
mAP_ivt.topk(5)
mAP_ivt.topClass(5)



# Disentangle

dist = t50metrics.Disentangle()
logit_i = dist.extract(inputs=predictions, componet="i")
target_i = dist.extract(inputs=targets, componet="i")

