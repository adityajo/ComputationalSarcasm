# import os
# java_path = "C:/Program Files/Java/jdk1.8.0_91/bin/java.exe"
# os.environ['JAVAHOME'] = java_path


# from nltk.parse.stanford import StanfordDependencyParser
# path_to_jar = 'F:\stanford-parser-full-2015-04-20\stanford-parser.jar'
# path_to_models_jar = 'F:\stanford-parser-full-2015-04-20\stanford-parser-3.5.2-models.jar'
# dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
#
# result = dependency_parser.raw_parse('I shot an elephant in my sleep')
# dep = result.next()
# print(list(dep.triples()))
import nltk
from nltk.parse.stanford import StanfordDependencyParser
dep_parser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
l= [parse.tree() for parse in dep_parser.raw_parse("So to know that I must be at my office this weekend.")]
#print(l[0])


# ROOT = 'ROOT'
# tree = l[0]
# def getNodes(parent):
#     for node in parent:
#         if type(node) is nltk.Tree:
#             if node.label() == ROOT:
#                 print "======== Sentence ========="
#                 print "Sentence:", " ".join(node.leaves())
#             else:
#                 print "Label:", node.label()
#                 print "Leaves:", node.leaves()
#
#             getNodes(node)
#         else:
#             print "Word:", node
#
# getNodes(tree)

print(l[0].label())
