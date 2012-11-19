import unittest
import evaluator

class TestEvaluator(unittest.TestCase):

    def testArithmetic(self):

        tree = ["+", 1, 3]
        self.assertEqual(evaluator.evaluate(tree), 4)

        tree = ["-", 3, 1]
        self.assertEqual(evaluator.evaluate(tree), 2)

        tree = ["*", 3, 1]
        self.assertEqual(evaluator.evaluate(tree), 3)

        tree = ["/", 3, 1]
        self.assertEqual(evaluator.evaluate(tree), 3)

        #compound operations
        tree = ["+", ["*", 4, 2], ["/", 16, 8]]
        self.assertEqual(evaluator.evaluate(tree), 10)

    def testAssignment(self):
        
        tree = [["var", "name", "Jane"], ["name"]]
        self.assertEqual(evaluator.evaluate(tree), "Jane")
        
    def testBool(self):
        
        tree = ['true']
        self.assertTrue(evaluator.evaluate(tree))
        
        tree = ['false']
        self.assertFalse(evaluator.evaluate(tree))
        
        #>
        tree = ['>', 5, 4]
        self.assertTrue(evaluator.evaluate(tree))
        
        tree = ['>', 3, 6]
        self.assertFalse(evaluator.evalutate(tree))
        
        tree = ['>', 6, 6]
        self.assertFalse(evaluator.evalutate(tree))
        
        #<
        tree = ['<', 4, 11]
        self.assertTrue(evaluator.evaluate(tree))
        
        tree = ['<', 9, 8]
        self.assertFalse(evaluator.evaluate(tree))
        
        tree = ['<', 1, 1]
        self.assertFalse(evaluator.evaluate(tree))
        
        #>=
        tree = ['>=', 5, 4]
        self.assertTrue(evaluator.evaluate(tree))
        
        tree = ['>=', 3, 6]
        self.assertFalse(evaluator.evalutate(tree))
        
        tree = ['>=', 6, 6]
        self.assertTrue(evaluator.evalutate(tree))
        
        #<=
        tree = ['<=', 4, 11]
        self.assertTrue(evaluator.evaluate(tree))
        
        tree = ['<=', 9, 8]
        self.assertFalse(evaluator.evaluate(tree))
        
        tree = ['<=', 1, 1]
        self.assertTrue(evaluator.evaluate(tree))
        
        #and
        tree = ['&&', "true", "false"]
        self.assertFalse(evaluator.evaluate(tree))
        
        tree = ['&&', 'true', 'true']
        self.assertTrue(evaluator.evaluate(tree))
        
        tree = ['&&', 'false', 'false']
        self.assertFalse(evaluator.evaluate(tree))
        
        tree = ['&&', 'true', 'true', 'true']
        self.assertTrue(evaluator.evaluate(tree))
        
        #or
        tree = ['||', "true", "false"]
        self.assertTrue(evaluator.evaluate(tree))
        
        tree = ['||', 'true', 'true']
        self.assertTrue(evaluator.evaluate(tree))
        
        tree = ['||', 'false', 'false']
        self.assertFalse(evaluator.evaluate(tree))
        
        tree = ['||', 'true', 'true', 'true']
        self.assertTrue(evaluator.evaluate(tree))
        
        #!
        tree = ['!', 'true']
        self.assertFalse(evaluator.evaluate(tree))
        
        tree = ['!', 'false']
        self.assertTrue(evaluator.evaluate(tree))
        
    def testConditionals(self):
        
        tree = ["if", ["true"], True, False]
        self.assertTrue(evaluator.evaluate(tree))
        
        tree = ["if", ["false"], True, False]
        self.assertFalse(evaluator.evaluate(tree))

        
    def testFunction(self):
        
        tree = [["function", "test", ["return", 2]], ["execute", "true"]]
        self.assertEqual(evaluator.evaluate(tree), 2)
        
        tree = [["function", "foo", [["var", "temp", 3], ["return", ['+', "temp", 2]]]], ["execute", "foo"]]
        self.assertEqual(evaluator.evaluate(tree), 5)

unittest.main()