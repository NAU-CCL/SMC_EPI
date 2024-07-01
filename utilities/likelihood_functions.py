from scipy.stats import nbinom,poisson,norm
from scipy.special import loggamma
import numpy as np
from numpy.typing import NDArray


def likelihood_NB(observation:NDArray[np.int_],particle_observation:NDArray[np.int_],var:float)->NDArray[np.float_]: 
    """Calculates the probability of the negative binomial random variable using a time dependent variance and the particle observation. 
    
    Args: 
        observation: A numpy array of real observations at the current time point, count data. 
        particle_observation: A numpy array of observations generated from a given particle at the current time point. 
        var: A float representing the time dependent variance. 

        Returns: 
            Array of probabilities corresponding to the given particle. 

    """
    X = nbinom.pmf(observation, n = (particle_observation)**2 / (var  - particle_observation), p = particle_observation / var)

    return X

def log_likelihood_norm(observation:NDArray[np.int_],particle_observation:NDArray[np.int_])->NDArray[np.float_]:
    return norm.logpdf(observation,particle_observation,100000000000)

def likelihood_poisson(observation:NDArray[np.int_],particle_observation:NDArray[np.int_])->NDArray[np.float_]:

    """Calculates the probability of the poisson random variable using the particle observation.
    
        Args: 
        observation: A numpy array of real observations at the current time point, count data. 
        particle_observation: A numpy array of observations generated from a given particle at the current time point. 
        var: Deprecated, left it here just in case. 

        Returns: 
            Array of probabilities corresponding to the given particle. 

    """

    return poisson.logpmf(observation,particle_observation)

def log_likelihood_poisson(observation:NDArray[np.int_],particle_observation:NDArray[np.int_])->NDArray[np.float_]:
    """Calculates the log-probability of the poisson random variable using the particle observation.
    
        Args: 
        observation: A numpy array of real observations at the current time point, count data. 
        particle_observation: A numpy array of observations generated from a given particle at the current time point. 
        var: Deprecated, left it here just in case. 

        Returns: 
            Array of probabilities corresponding to the given particle. 

    """

    return poisson.logpmf(observation,particle_observation)


def log_likelihood_NB(observation:NDArray[np.int_],particle_observation:NDArray[np.int_],R:float)->int: 

    """Calculates the log-probability of the negative binomial random variable using a fixed value of R and the particle observation, calculates the NB pmf by hand for testing.

    Args: 
    observation: A numpy array of real observations at the current time point, count data. 
    particle_observation: A numpy array of observations generated from a given particle at the current time point. 
    R: A float representing the parameter R in the NB distribution. 

    Returns: 
        Array of probabilities corresponding to the given particle. 

    """
    
    prob = np.array([R/(R+particle_observation)])
    prob[prob<=1e-10] = 1e-10
    prob[prob>=1-1e-10] = 1-1e-10
    v1 = prob[observation>=0] #do not include the days if observation is negative
    v2 = observation[observation>=0]
    x = loggamma(v2+R)-loggamma(v2+1)-loggamma(R)+R*np.log(v1)+v2*np.log(1-v1)

    return x