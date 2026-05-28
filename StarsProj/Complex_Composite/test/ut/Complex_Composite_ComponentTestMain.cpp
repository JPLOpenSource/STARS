// ======================================================================
// \title  Complex_Composite_ComponentTestMain.cpp
// \author watney
// \brief  cpp file for Complex_Composite_Component component test main function
// ======================================================================

#include "Complex_Composite_ComponentTester.hpp"

TEST(Nominal, testAllTransitions) {
    Components::Complex_Composite_ComponentTester tester;
    tester.testAllTransitions();
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
