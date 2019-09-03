from agent.RandomAgent import RandomAgent
from game.SinglePlayerGuiWrapper import SinglePlayerGuiWrapper

if __name__ == '__main__':
    agent = RandomAgent()
    wrapper = SinglePlayerGuiWrapper(agent)
    wrapper.run()
