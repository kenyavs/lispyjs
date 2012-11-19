import unittest
import evaluator

class TestEvaluator(unittest.TestCase):

	def testArithmetic(self):

		#add
		tree = ["+", 1, 3]
		self.assertEqual(evaluator.evaluate(tree), 4)

		tree = ["-", 3, 1]
		self.assertEqual(evaluator.evaluate(tree), 2)

		tree = ["*", 3, 1]
		self.assertEqual(evaluator.evaluate(tree), 3)

		tree = ["/", 3, 1]
		self.assertEqual(evaluator.evaluate(tree), 3)



unittest.main()



