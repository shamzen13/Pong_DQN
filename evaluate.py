import gym
import matplotlib.pyplot as plt
from stable_baselines3 import DQN
from Pong_env import PongEnv

model = DQN.load("dqn_pong_agent")

env = PongEnv()

tot_rewards = []

num_steps = 1000
obs = env.reset()
tot_reward = 0

n_episodes = 10 
for episode in range(n_episodes):
    obs = env.reset()
    tot_reward = 0
    done = False
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        tot_reward += reward
        env.render()
    tot_rewards.append(tot_reward)
    print(f"Episode {episode + 1} reward: {tot_reward}")


env.close()

print(f"Total Reward over {len(tot_rewards)} episodes: {sum(tot_rewards)}")

plt.plot(tot_rewards)
plt.title("Total Reward per Episode")
plt.xlabel("Episode")
plt.ylabel("Total Reward")
plt.show()
