from Implementations.algorithms.TimeDependentBeta import TimeDependentAlgo
from Implementations.resamplers.resamplers import NBinomResample,LogNBinomResample
from Implementations.solvers.StochasticSolvers import PoissonSolver
from Implementations.solvers.DeterministicSolvers import EulerSolver
from Implementations.perturbers.perturbers import MultivariatePerturbations
from utilities.Utils import Context,ESTIMATION
from functools import partial
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.set_printoptions(suppress=True)

algo = TimeDependentAlgo(integrator = EulerSolver(),
                        perturb = MultivariatePerturbations(hyper_params={"h":0.5,"sigma1":0.1,"sigma2":0.1}),
                        resampler = NBinomResample(),
                        ctx=Context(population=7_000_000,
                                    state_size = 4,
                                    weights=np.zeros(10000),
                                    rng=np.random.default_rng(),
                        particle_count=10000))

algo.initialize(params={
"beta":ESTIMATION.VARIABLE,
"gamma":ESTIMATION.STATIC,
"std":ESTIMATION.VARIABLE, 
"hosp":ESTIMATION.STATIC,
"L":90.0,
"D":ESTIMATION.STATIC}
,priors={"beta":partial(algo.ctx.rng.uniform,0.,1.),
          "D":partial(algo.ctx.rng.uniform,1.,20.),
          "std":partial(algo.ctx.rng.uniform,20.,30.),
          "gamma":partial(algo.ctx.rng.uniform,0.,1.),
          "hosp":partial(algo.ctx.rng.uniform,1.,10.)
          })
data = pd.read_csv('./datasets/FLU_HOSPITALIZATIONS.csv').to_numpy()
data = np.delete(data,0,1)


print("\n")
#algo.print_particles()
beta = []
D = []
hosp = []
gamma = []
state = []
for t in range(len(data)): 
     print(f"iteration: {t}")
     algo.particles = algo.integrator.propagate(algo.particles,algo.ctx)   
     algo.ctx.weights = (algo.resampler.compute_weights(data[t],algo.particles))
     #print(algo.ctx.weights)
     algo.particles = algo.resampler.resample(algo.ctx,algo.particles)
     algo.particles = algo.perturb.randomly_perturb(algo.ctx,algo.particles) 
    #  print(np.mean([particle.observation for particle in algo.particles]))
    #  print(data[t])
     beta.append(np.mean([particle.param['beta'] for particle in algo.particles]))
     D.append(np.mean([particle.param['D'] for particle in algo.particles]))
     hosp.append(np.mean([particle.param['hosp'] for particle in algo.particles]))
     gamma.append(np.mean([particle.param['gamma'] for particle in algo.particles]))
     print(D[-1])
     print(hosp[-1])
     print(gamma[-1])
     #algo.print_particles()
     state.append(np.mean([particle.state for particle in algo.particles],axis=0))
     print(state[-1])
#     print(algo.ctx.weights)
plt.plot(beta)
plt.show()

plt.yscale('log')
plt.plot(state)
plt.show()


    