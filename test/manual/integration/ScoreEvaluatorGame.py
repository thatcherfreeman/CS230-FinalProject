from agent.TimedAgent import TimedAgent
from agent.evaluator.intuitive.ScoreEvaluator import ScoreEvaluator
from agent.simulator.SimulatorAgent import SimulatorAgent
from game.SinglePlayerGuiWrapper import SinglePlayerGuiWrapper

if __name__ == '__main__':
    agent = TimedAgent(SimulatorAgent(ScoreEvaluator()))
    wrapper = SinglePlayerGuiWrapper(agent)
    wrapper.run()
