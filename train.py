import gym
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import DQN
from Pong_env import PongEnv
import time

# initialoizing the env

env = PongEnv()

model = DQN(

    "MlpPolicy",    # multiple layered NN
    env,
    verbose=1,
    learning_rate=1e-4,
    buffer_size=50_000,
    learning_starts=1000,
    batch_size=64,
    train_freq=4,
    target_update_interval=100,
    exploration_fraction=0.2,
    exploration_final_eps=0.02,
    tensorboard_log="./pong_dqn_tensorboard/"


)

# training agent
model.learn(total_timesteps=100_500)

model.save("dqn_pong_agent")

#render & test

obs = env.reset()

for _ in range(1000):
    action, _states = model.predict(obs)
    obs, reward, done, info = env.step(action)
    env.render()


    if done : 
        obs = env.reset()

env.close()