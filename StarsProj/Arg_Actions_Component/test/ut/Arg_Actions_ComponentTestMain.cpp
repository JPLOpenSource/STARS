// ======================================================================
// \title  Arg_Actions_ComponentTestMain.cpp
// \author watney
// \brief  cpp file for Arg_Actions_Component component test main function
// ======================================================================

#include "Arg_Actions_ComponentTester.hpp"

TEST(Nominal, testTransitions) {
    Components::Arg_Actions_ComponentTester tester;
    tester.testTransitions();
}

TEST(Nominal, testEV2Transitions) {
    Components::Arg_Actions_ComponentTester tester;
    tester.testEV2Transitions();
}

TEST(Nominal, testDataCommand) {
    Components::Arg_Actions_ComponentTester tester;
    tester.testDataCommand();
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
