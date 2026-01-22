package com.aptos.specs.support;

import io.cucumber.java.Before;
import io.cucumber.java.After;
import io.cucumber.java.Scenario;

/**
 * Cucumber hooks for setup and teardown.
 */
public class Hooks {
    
    private final World world;
    
    public Hooks(World world) {
        this.world = world;
    }
    
    /**
     * Reset world state before each scenario.
     */
    @Before
    public void beforeScenario(Scenario scenario) {
        world.reset();
    }
    
    /**
     * Cleanup after each scenario.
     */
    @After
    public void afterScenario(Scenario scenario) {
        // Log scenario result if needed
        if (scenario.isFailed() && world.getError() != null) {
            System.err.println("Scenario failed with error: " + world.getError().getMessage());
        }
    }
}
