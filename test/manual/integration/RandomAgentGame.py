from agent.RandomAgent import RandomAgent
from game.GravitySinglePlayerGuiWrapper import GravitySinglePlayerGuiWrapper

if __name__ == '__main__':
    agent = RandomAgent()
    wrapper = GravitySinglePlayerGuiWrapper(agent)
    wrapper.run()
