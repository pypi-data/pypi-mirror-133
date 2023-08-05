import time
import numpy as np
from gym.vector.async_vector_env import AsyncVectorEnv
from gym.vector.sync_vector_env import SyncVectorEnv
from gym.vector.vector_env import VectorEnv, VectorEnvWrapper
def fps(env,steps_per_test=100,episode=10):
    
    result_multiply=env.num_envs if isinstance(env,AsyncVectorEnv) else 1
    for e in range(episode):
        count=0
        start_t=time.time()
        for i in range(steps_per_test):
            a = env.action_space.sample()  # Sample an action
            obs, reward, done, info = env.step(a)  # Step the environoment with the sampled random action
            if isinstance(done,int):
                if done:
                    obs = env.reset()
            elif isinstance(done,np.ndarray):
                if done.any():
                    obs = env.reset()  # Reset environment
        env.reset() 
        dt=time.time()-start_t
        print("fps = {}".format(steps_per_test/dt*result_multiply))