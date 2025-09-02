# Load required libraries
library(spatstat)     # For simulating and analyzing spatial point patterns
library(ggplot2)      # For plotting results (not yet used in this snippet)
library(gridExtra)    # For arranging multiple plots (also not yet used)
library(extraDistr)   # For calculations with the Skellam distribution
library(dplyr)  

# Define the study window: a 1000 x 1000 square
win <- owin(c(0, 1000), c(0, 1000))

# Generate three types of spatial point patterns

set.seed(123)  # For reproducibility

# 1. CSR (Complete Spatial Randomness) using Poisson point process
# lambda is the density of points per unit area
# In the square 1000x1000 , the value lambda=0.0003 implies approx 0.0003*1000*1000=300 pontos
pattern_csr <- rpoispp(lambda = 0.0003, win = win)
plot(pattern_csr)

# 2. Clustered pattern using Thomas process (cluster process)
# kappa = densidade de pontos-pais; mu=numero approx de filhos ao redor de cada ponto-pai
# scale=dispersao dos filhos em volta dos pais
pattern_clustered <- rThomas(kappa = 0.0001, scale = 25, mu = 3, win = win)
plot(pattern_clustered)
# A more tightly clustered process: decreases scale
pattern_clustered <- rThomas(kappa = 0.0001, scale = 15, mu = 3, win = win)
plot(pattern_clustered)
# A larger number number of children per parent: increase mu
pattern_clustered <- rThomas(kappa = 0.0001, scale = 15, mu = 15, win = win)
plot(pattern_clustered)
# A less dense number of clusters: decrease kappa
pattern_clustered <- rThomas(kappa = 0.00001, scale = 15, mu = 15, win = win)
plot(pattern_clustered)

# 3. Regular pattern using Simple Sequential Inhibition (SSI) process
pattern_regular <- rSSI(r = 15, n = 300, win = win)
plot(pattern_regular)

###################################################
# Experiment
###################################################

source("r-code/robust_mapping.R")

plot_grid<-function(pattern, grid){
  plot_limit = grid$opt_granularity * (1000/grid$opt_granularity + 1)
  grid_tess <- spatstat.geom::tess(
    xgrid = seq(0, plot_limit, by = grid$opt_granularity),
    ygrid = seq(0, plot_limit, by = grid$opt_granularity)
  )
  
  plot(pattern, main = "")
  plot(grid_tess, add = TRUE, lty = 2, border = "blue")
}

# Gere um processo de Thomas com 10 pais e approx 30 filhos por pai com scale=15 
# (bem apertados em volta dos pais)
# Teremos 300 pontos approx
# Obtenha o cell size ótimo
pattern_clustered <- rThomas(kappa = 0.00001, scale = 15, mu = 30, win = win)
plot(pattern_clustered)

df_pattern_clustered <- as.data.frame(pattern_clustered)
my_scales = c(20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 170, 180, 200, 230, 250, 280, 300)
grid_thomas = robust.quadcount(df_pattern_clustered, verbose=TRUE, my_scales=my_scales, uniformity_method="Nearest-neighbor")

print(grid_thomas)
print(grid_thomas$opt_granularity) # 46.65672
grid_thomas$opt_granularity <- 2
plot_grid(pattern_clustered, grid_thomas)

plot(grid_thomas$uniformity.curve)


# Gere um processo CSR com lambda = 0.0003 (300 pontos approx)
# Obtenha o cell size ótimo
# pattern_csr <- rpoispp(lambda = 0.0003, win = win)
# plot(pattern_csr)

# df_pattern_csr <- as.data.frame(pattern_csr)
# grid_csr = robust.quadcount(df_pattern_csr, verbose=TRUE)

# print(grid_csr$opt_granularity) # 99.69718
# plot_grid(pattern_csr, grid_csr)


# # Gerar um processo com rSSI com r=20 e n=300
# pattern_ssi <- rSSI(r = 20, n = 300, win = win)
# plot(pattern_ssi)

# df_pattern_ssi <- as.data.frame(pattern_ssi)
# grid_ssi = robust.quadcount(df_pattern_ssi, verbose=TRUE)

# print(grid_ssi$opt_granularity) # 99.35235
# plot_grid(pattern_ssi, grid_ssi)


# ### MISTURE OS DOIS TIPOS DE PONTOS gerando um novo padrão espacial.
# ### Obtenha o cell size ótimo desse padrão misturado.
# df_csr_thomas <- rbind(df_pattern_csr, df_pattern_clustered)
# plot(df_csr_thomas)

# grid_csr_thomas = robust.quadcount(df_csr_thomas, verbose=TRUE)

# print(grid_csr_thomas$opt_granularity) # 99.84138
# plot_grid(df_csr_thomas, grid_csr_thomas)


# Testing

data <- read.csv("samples/MULTI_THOMAS.csv")

point_set <- data.frame(x = data[,1], y = data[,2])

plot(point_set)

result = robust.quadcount(point_set, verbose=TRUE, uniformity_method="Nearest-neighbor")

print(result)

result2 = robust.quadcount(point_set, verbose=TRUE, uniformity_method="Quadratcount")

print(result2)


### Como os três cell sizes se relacionam?

# Um problema que percebi é que as escalas testadas vão até 100
# Isso foi configurado no robust_mapping.R, mas percebi que apenas ao final

# CSR: 99.69718
# ---------------
# No método de CSR, o enquadramento ficou razoável. A uniformidade apresentou algumas quedas quando o tamanho da grade estava próximo de 100, o que é esperado.
# 
#
# THOMAS: 46.65672
# -----------------
# Nesse método, a robustez cresceu mais linearmente. Já a uniformidade teve uma decaimento linear significativo quando o tamanho da grade estava próximo de 50.
# O enquadramento dividiu alguns clusters, o que não necessariamente é um problema, mas pode ser interessante observar. 
# 
#
# SSI: 99.35235
# --------------
# O método de SSI apresentou um comportamento semelhante ao CSR, mas com uma uniformidade sempre 1, ou seja, é mais uniforme.
# 
# 
# CSR + THOMAS: 99.84138
# -----------------------
# Os gráficos de uniformidade e robustez são uma mistura dos dois métodos.
# A robustez é mais linear do que no CSR e a uniformidade tem quedas significativas quando o tamanho da grade está próximo de 50.
# O enquadramento ficou aparentemente bom. Esse enquadramento divide menos os clusters do que o método de Thomas.
#
