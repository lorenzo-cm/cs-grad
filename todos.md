# Todos


## Implementation gen_scale
- Change gen_scales to bbox_base
- Change gen_scales to make the start stop based in density

## Time space granularities

- Nd bbox does not need to be regular
  - Change quadrat count division to respect the scales

I have $t$ which is the current granularity for time and $s$ the current granularity for space

$\tau$ is the list of granularities $t$ and $S$ is the list of granularities $s$

I want the best combinartion of $Optimizer(s, t)$

To define $S$ i will use the current method of picking the min size and multiplying by a small factor to get the min and max value of $s$

For $\tau$, i will just do:
 $$i=0 \rightarrow t_i = (time_{max} - time_{min}) / (i + 2)$$

$\space$

```py
time_max = 50_000
time_min = 0
scale_size = 10

tau = [(time_max - time_min) / (i + 2) for i in np.arange(scale_size)]
```