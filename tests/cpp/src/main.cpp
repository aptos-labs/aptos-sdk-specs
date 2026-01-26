/// Main test runner for Aptos C++ SDK behavioral specifications.
///
/// This runs all Gherkin feature files against the SDK using CWT-Cucumber.

#include <cucumber.hpp>

#include "../support/world.hpp"

using namespace aptos::specs;

// =============================================================================
// Hooks
// =============================================================================

BEFORE(reset_world) {
  // Get or create world context and reset it
  cuke::context<TestWorld>().reset();
}

AFTER(cleanup_world) {
  // Cleanup after each scenario if needed
}

// =============================================================================
// Main Entry Point
// =============================================================================

int main(int argc, const char *argv[]) {
  // Run CWT-Cucumber tests
  auto result = cuke::entry_point(argc, argv);
  return result == cuke::results::test_status::passed ? 0 : 1;
}
