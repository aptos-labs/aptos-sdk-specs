package com.aptos.specs.support

import io.cucumber.java.After
import io.cucumber.java.Before
import io.cucumber.java.Scenario

/**
 * Cucumber hooks for scenario lifecycle management.
 */
class Hooks(private val world: World) {
    /**
     * Run before each scenario.
     * Ensures the World is in a clean state.
     */
    @Before
    fun beforeScenario(scenario: Scenario) {
        world.reset()

        // Log scenario start for debugging (optional)
        // println("Starting scenario: ${scenario.name}")
    }

    /**
     * Run after each scenario.
     * Can be used for cleanup or logging.
     */
    @After
    fun afterScenario(scenario: Scenario) {
        // Log scenario result for debugging (optional)
        // println("Finished scenario: ${scenario.name} - ${scenario.status}")

        // Perform any necessary cleanup
        world.reset()
    }
}
