// ======================================================================
// \title  Simple_ComponentTestMain.cpp
// \author watney
// \brief  cpp file for Simple_Component component test main function
// ======================================================================

#include "Simple_ComponentTester.hpp"

TEST(Nominal, toDo) {
    Components::Simple_ComponentTester tester;
    tester.toDo();
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
