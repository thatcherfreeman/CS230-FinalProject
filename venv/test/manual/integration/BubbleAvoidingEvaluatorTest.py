from agent.TimedAgent import TimedAgent
from agent.evaluator.intuitive.BubbleAvoidingEvaluator import BubbleAvoidingEvaluator
from agent.simulator.SimulatorAgent import SimulatorAgent
from game.SinglePlayerGuiWrapper import SinglePlayerGuiWrapper

if __name__ == '__main__':
    agent = TimedAgent(SimulatorAgent(BubbleAvoidingEvaluator()))
    wrapper = SinglePlayerGuiWrapper(agent)
    wrapper.run()
