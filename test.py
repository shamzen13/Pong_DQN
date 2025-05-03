
import Pong_env

env = Pong_env.PongEnv()

obs = env.reset()
done = False

while not done:
    action = env.action_space.sample()  # Random action
    obs, reward, done, _ = env.step(action)
    env.render()

env.close()

