#interface objects
from .InterfaceObjects import ASG,StopCondition
#import helper functions
from .HelperFunctions import *

#-----------------------------------------------------------------------------------------------------------
#
#   ASG extension
#
#       TODO:
#               - Discuss: Do we need to provide the rules in the getASG()
#               - Discuss: Do we need to provide the rules in the setASG()
#               - Discuss: Can we assume that the assembly system is in place when performing setASG()
#               - Discuss: Do we need seperate functions to UPDATE and ADD stopcriterions?
#               - Discuss: Do we need seperate functions to UPDATE and ADD DFA rules?
#               - ERROR: new classes are not generated (+linked) correctly -> subcomposition of platformRoot does not work
#
# -----------------------------------------------------------------------------------------------------------

def getASG(AssemblySystemName,model,KBPath):
    """
          Function to fetch the Assembly Sequence Generation (ASG) configuration using the name as identifier.
          The function returns an interface block of the ASG

          :param string AssemblySystemName: Name identifier of the assemlbySystem
          :param object model: Metamodel instance model
          :param string KBPath: Absolute path to the metamodel instance model

          :return object ASGModel: Interface object of the ASG (-1 = error)
    """

    found = 0
    #ASG = []        #[Name, Description,processingType,[operationGeneratorName,operationGeneratorType],[operationSelectorName,operationSelectorType],[operationEvaluatorName,operationEvaluatorType],[terminatorName,[terminators]]]]       with terminators = [name,description,value,stopCriterion enum]
    InterfaceObject = ASG(None) #interface object placeholder
    if len(model.includesAssemblySystem.items) != 0:
        #match the assemblySystem by Name
        for assemblySystem in model.includesAssemblySystem.items:
            if AssemblySystemName == assemblySystem.hasName:
                found=1
                #fetch ASG and setup ASG return
                ASG_temp = assemblySystem.hasAssemblyAlgorithmConfiguration
                InterfaceObject.Name = ASG_temp.hasName
                InterfaceObject.Description = ASG_temp.hasDescription
                InterfaceObject.ProcessingType = ASG_temp.hasProcessingType.name

                # try-catch structure to fetch the ASG GENERATOR
                try:
                        InterfaceObject.Generator=[ASG_temp.hasSinglePartGenerator.hasName, 'SinglePartGenerator']
                except:
                    x = "No SinglePartGenerator available"
                try:
                        InterfaceObject.Generator=[ASG_temp.hasMultiPartGenerator.hasName, 'MultiPartGenerator']
                except:
                    x = "No MultiPartGenerator available"

                # try-catch structure to fetch the ASG SELECTOR
                try:
                        InterfaceObject.Selector=[ASG_temp.hasDefaultSelector.hasName, 'DefaultSelector']
                except:
                    x = "No Default selector available"
                try:
                        InterfaceObject.Selector=[ASG_temp.hasRuleSelector.hasName, 'RuleSelector']             #TODO: discuss if we need to fetch the rules
                except:
                    x = "No Rule selector available"

                # try-catch structure to fetch the ASG EVALUATOR
                try:
                        InterfaceObject.Evaluator=[ASG_temp.hasUniformEvaluator.hasName,'UniformEvaluator']
                except:
                    x = "No uniform evalutor available"
                try:
                        InterfaceObject.Evaluator=[ASG_temp.hasRuleEvaluator.hasName, 'RuleEvaluator']
                except:
                    x = "No Rule selector available"



                terms = []
                for terminator in ASG_temp.hasTerminator.hasStopCriterion.items:
                    #initialize
                    termList = []

                    #fetch the termintator name
                    s = StopCondition(None, terminator.hasName, terminator.hasDescription,terminator.hasValue, terminator.hasStopCriterion.name)

                    #add to criteria
                    terms.append(s)
                InterfaceObject.StopConditionList = terms

            else:
                x = 1



        if found:
            return InterfaceObject
        else:
            return -2
    else:
        return -2  # no assembly systems!

def updateASG(AssemblySystemName,interfaceObject,model,KBPath):
    """
          Function to update the  complete Assembly Sequence Generation (ASG) configuration using the name as identifier.
          The ASG interface object is used to interface with the function.
          The function returns whether or not the function is performed correctly

          :param string AssemblySystemName: Name identifier of the assemlbySystem
          :param object ASGModel: Interface object of the ASG
          :param object model: Metamodel instance model
          :param string KBPath: Absolute path to the metamodel instance model

          :return int Error: -1 = error, 1= function performed correcly
    """

    found = 0
    if len(model.includesAssemblySystem.items) != 0:
        #match the assemblySystem by Name
        for assemblySystem in model.includesAssemblySystem.items:
            if AssemblySystemName == assemblySystem.hasName:
                found=1
                #fetch ASG and setup ASG return
                assemblySystem.hasAssemblyAlgorithmConfiguration.hasName = interfaceObject.Name
                assemblySystem.hasAssemblyAlgorithmConfiguration.hasDescription = interfaceObject.Description
                assemblySystem.hasAssemblyAlgorithmConfiguration.hasProcessingType = interfaceObject.ProcessingType

                # try-catch structure to fetch the ASG GENERATOR
                try:
                    assemblySystem.hasAssemblyAlgorithmConfigurationhasSinglePartGenerator.hasSinglePartGenerator.hasName = interfaceObject.Generator[0]
                except:
                    x = "No SinglePartGenerator available"
                try:
                    assemblySystem.hasAssemblyAlgorithmConfigurationhasSinglePartGenerator.hasMultiPartGenerator.hasName = interfaceObject.Generator[0]
                except:
                    x = "No MultiPartGenerator available"

                # try-catch structure to fetch the ASG SELECTOR
                try:
                    assemblySystem.hasAssemblyAlgorithmConfigurationhasSinglePartGenerator.hasDefaultSelector.hasName =  interfaceObject.Selector[0]
                except:
                    x = "No Default selector available"
                try:
                    assemblySystem.hasAssemblyAlgorithmConfigurationhasSinglePartGenerator.hasRuleSelector.hasName = interfaceObject.Selector[0]
                    #TODO: discuss if we need to update the rules or via dedicated function!
                except:
                    x = "No Rule selector available"

                # try-catch structure to fetch the ASG EVALUATOR
                try:
                    assemblySystem.hasAssemblyAlgorithmConfigurationhasSinglePartGenerator.hasUniformEvaluator.hasName = interfaceObject.Evaluator[0]
                except:
                    x = "No uniform evalutor available"
                try:
                    assemblySystem.hasAssemblyAlgorithmConfigurationhasSinglePartGenerator.hasRuleEvaluator.hasName = interfaceObject.Evaluator[0]
                    # TODO: discuss if we need to update the rules or via dedicated function!
                except:
                    x = "No Rule selector available"



                terms = []
                for terminator in assemblySystem.hasAssemblyAlgorithmConfiguration.hasTerminator.hasStopCriterion.items:
                    for stp in interfaceObject.StopConditionList:
                        if stp.Name==terminator.hasName:
                            terminator.hasName=stp.Name
                            terminator.hasDescription=stp.Description
                            terminator.hasValue=stp.Value
                            terminator.hasStopCriterion=stp.StopCriteria

            else:
                return -1

        if found:
            updateKBv6(KBPath, model)
            return 1
        else:
            return -1
    else:
        return -1  # no Optimization Problem!

def setASG( AssemblySystemName, InterfaceObject,model,KBPath,MM):
    """
          Function to set a new Assembly Sequence Generation (ASG) configuration to an blank KB (no existing performance part).
          The performance interface object is used to interface with the function.
          The function returns whether or not the function is performed correctly

          :param object ASGModel: Interface object of the ASG model
          :param object model: Metamodel instance model
          :param string KBPath: Absolute path to the metamodel instance model

          :return int Error: -1 = error, 1= function performed correcly
    """
    #match the AssemblySystem-of-interest
    if len(model.includesAssemblySystem.items) != 0:
        #match the assemblySystem by Name
        for assemblySystem in model.includesAssemblySystem.items:
            if AssemblySystemName == assemblySystem.hasName:
                #check if ASG config exist
                if assemblySystem.hasAssemblyAlgorithmConfiguration is not None:
                    #update current ASG config
                    ASG= assemblySystem.hasAssemblyAlgorithmConfiguration
                    #ASG attributes
                    ASG.hasName = InterfaceObject.Name
                    ASG.hasDescription = InterfaceObject.Description
                    #ASG.hasProcessingType = configuration[2]                        #TODO: check how to set this

                    if 'SinglePartGenerator' in InterfaceObject.Generator[1]:
                        # try-catch structure to fetch the ASG GENERATOR
                        try:
                            ASG.hasSinglePartGenerator.hasName = InterfaceObject.Generator[0]
                        except:
                            x = "No SinglePartGenerator available"                   #TODO: does not work -> generate new class fails!
                            #create new class if not existing
                            g_ = create_custom(ASG,"SinglePartGenerator",MM)
                            g_.hasName = InterfaceObject.Generator[0]
                            ASG.hasSinglePartGenerator = g_

                    if 'MultiPartGenerator' in InterfaceObject.Generator[1]:
                        # try-catch structure to fetch the ASG GENERATOR
                        try:
                            ASG.hasMultiPartGenerator.hasName = InterfaceObject.Generator[0]
                        except:
                            x = "No MultiPartGenerator available"                   #TODO: does not work -> generate new class fails!
                            #create new class if not existing
                            g_ = create_custom(ASG,"MultiPartGenerator",MM)
                            g_.hasName = InterfaceObject.Generator[0]
                            ASG.hasMultiPartGenerator = g_

                    if 'DefaultSelector' in InterfaceObject.Selector[1]:
                        # try-catch structure to fetch the ASG GENERATOR
                        try:
                            ASG.hasDefaultSelector.hasName = InterfaceObject.Selector[0]
                        except:
                            x = "No Default selector available"                      #TODO: does not work -> generate new class fails!
                            #create new class if not existing
                            g_ = create_custom(ASG,"DefaultSelector",MM)
                            g_.hasName = InterfaceObject.Selector[0]
                            ASG.hasDefaultSelector = g_

                    if 'RuleSelector' in InterfaceObject.Selector[1]:
                        # try-catch structure to fetch the ASG GENERATOR
                        try:
                            ASG.hasRuleSelector.hasName = InterfaceObject.Selector[0]
                        except:
                            x = "No RuleSelector available"                         #TODO: does not work -> generate new class fails!
                            #create new class if not existing
                            g_ = create_custom(ASG,"RuleSelector",MM)
                            g_.hasName = InterfaceObject.Selector[0]
                            ASG.hasRuleSelector = g_

                    if 'UniformEvaluator' in InterfaceObject.Evaluator[1]:
                        # try-catch structure to fetch the ASG GENERATOR
                        try:
                            ASG.hasUniformEvaluator.hasName = InterfaceObject.Evaluator[0]
                        except:
                            x = "No uniform evaluator available"                    #TODO: does not work -> generate new class fails!
                            #create new class if not existing
                            g_ = create_custom(ASG,"UniformEvaluator",MM)
                            g_.hasName = InterfaceObject.Evaluator[0]
                            ASG.hasDefaultSelector = g_

                    if 'RuleEvaluator' in InterfaceObject.Evaluator[1]:
                        # try-catch structure to fetch the ASG GENERATOR
                        try:
                            ASG.hasRuleEvaluator.hasName = InterfaceObject.Evaluator[0]
                        except:
                            x = "No RuleEvaluator available"                        #TODO: does not work -> generate new class fails!
                            #create new class if not existing
                            g_ = create_custom(ASG,"RuleEvaluator",MM)
                            g_.hasName = InterfaceObject.Evaluator[0]
                            ASG.hasRuleEvaluator = g_

                    #updating the existing stopConditions and adding new ones
                    for stopcriteria in InterfaceObject.StopConditionList:
                        Name=stopcriteria.Name
                        Description = stopcriteria.Description
                        Value = stopcriteria.Value
                        if '0' in stopcriteria.StopCriteria: Type=0
                        if '1' in stopcriteria.StopCriteria: Type=1
                        #look for existing stopcriteria
                        found = 0
                        for terminator in ASG.hasTerminator.hasStopCriterion.items:
                            if terminator.hasName == Name:
                                found = 1
                                #perform update of terminator
                                terminator.hasName = Name
                                terminator.hasDescription = Description
                                terminator.hasValue = Value
                                #terminator.hasStopCriterion = Type                 #TODO: check how to update the enum

                        if not found:                                               #TODO: does not work -> generate new class fails!
                            sc = create_custom(ASG.hasTerminator,"StopCriterion",MM)
                            sc.hasName = Name
                            sc.hasDescription = Description
                            sc.hasValue = Value
                            # sc.hasStopCriterion = Type      #TODO: check how to update the enum
                            ASG.hasTerminator.hasStopCriterion.items.append(sc)

                    updateKBv6(KBPath,model)
                else:
                    #generate a new ASG config and configure
                    ASG = create("AssemblyAlgorithmConfiguration",MM)
                    # ASG attributes
                    ASG.hasName = InterfaceObject.Name
                    ASG.hasDescription = InterfaceObject.Description
                    ASG.hasProcessingType = InterfaceObject.ProcessingType

                    if 'SinglePartGenerator' in InterfaceObject.Generator[1]:
                        # try-catch structure to fetch the ASG GENERATOR
                        try:
                            ASG.hasSinglePartGenerator.hasName = InterfaceObject.Generator[0]
                        except:
                            x = "No SinglePartGenerator available"       #TODO: does not work -> generate new class fails!
                            #create new class if not existing
                            g_ = create("SinglePartGenerator",MM,model)
                            g_.hasName = InterfaceObject.Generator[0]
                            ASG.hasSinglePartGenerator = g_

                    if 'MultiPartGenerator' in InterfaceObject.Generator[1]:
                        # try-catch structure to fetch the ASG GENERATOR
                        try:
                            ASG.hasMultiPartGenerator.hasName = InterfaceObject.Generator[0]
                        except:
                            x = "No MultiPartGenerator available"       #TODO: does not work -> generate new class fails!
                            #create new class if not existing
                            g_ = create("MultiPartGenerator",MM,model)
                            g_.hasName = InterfaceObject.Generator[0]
                            ASG.hasMultiPartGenerator = g_

                    if 'DefaultSelector' in InterfaceObject.Selector[1]:
                        # try-catch structure to fetch the ASG GENERATOR
                        try:
                            ASG.hasDefaultSelector.hasName = InterfaceObject.Selector[0]
                        except:
                            x = "No Default selector available"       #TODO: does not work -> generate new class fails!
                            #create new class if not existing
                            g_ = create("DefaultSelector",MM,model)
                            g_.hasName = InterfaceObject.Selector[0]
                            ASG.hasDefaultSelector = g_

                    if 'RuleSelector' in InterfaceObject.Selector[1]:
                        # try-catch structure to fetch the ASG GENERATOR
                        try:
                            ASG.hasRuleSelector.hasName = InterfaceObject.Selector[0]
                        except:
                            x = "No RuleSelector available"       #TODO: does not work -> generate new class fails!
                            #create new class if not existing
                            g_ = create("RuleSelector",MM,model)
                            g_.hasName = InterfaceObject.Selector[0]
                            ASG.hasRuleSelector = g_

                    if 'UniformEvaluator' in InterfaceObject.Evaluator[1]:
                        # try-catch structure to fetch the ASG GENERATOR
                        try:
                            ASG.hasUniformEvaluator.hasName = InterfaceObject.Evaluator[0]
                        except:
                            x = "No uniform evaluator available"       #TODO: does not work -> generate new class fails!
                            #create new class if not existing
                            g_ = create("UniformEvaluator",MM,model)
                            g_.hasName = InterfaceObject.Evaluator[0]
                            ASG.hasDefaultSelector = g_

                    if 'RuleEvaluator' in InterfaceObject.Evaluator[1]:
                        # try-catch structure to fetch the ASG GENERATOR
                        try:
                            ASG.hasRuleEvaluator.hasName = InterfaceObject.Evaluator[0]
                        except:
                            x = "No RuleEvaluator available"       #TODO: does not work -> generate new class fails!
                            #create new class if not existing
                            g_ = create("RuleEvaluator",MM,model)
                            g_.hasName = InterfaceObject.Evaluator[0]
                            ASG.hasRuleEvaluator = g_



                    model.includesAssemblySystem.items.append(ASG)
                    updateKBv6(KBPath,model)