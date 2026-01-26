package com.aptos.specs;

import org.junit.platform.suite.api.ConfigurationParameter;
import org.junit.platform.suite.api.IncludeEngines;
import org.junit.platform.suite.api.SelectClasspathResource;
import org.junit.platform.suite.api.Suite;

import static io.cucumber.junit.platform.engine.Constants.*;

/**
 * JUnit 5 test runner for Cucumber BDD tests.
 *
 * This class configures Cucumber to: - Load feature files from ../../features
 * (relative to project root) - Use step definitions from com.aptos.specs.steps
 * and com.aptos.specs.support - Generate HTML and JSON reports
 */
@Suite
@IncludeEngines("cucumber")
@ConfigurationParameter(key = FEATURES_PROPERTY_NAME, value = "../../features")
@ConfigurationParameter(key = GLUE_PROPERTY_NAME, value = "com.aptos.specs.steps,com.aptos.specs.support")
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, value = "pretty,html:target/cucumber-reports/cucumber.html,json:target/cucumber-reports/cucumber.json")
@ConfigurationParameter(key = JUNIT_PLATFORM_NAMING_STRATEGY_PROPERTY_NAME, value = "long")
public class RunCucumberTest {
	// This class is just a marker for JUnit Platform to discover Cucumber tests
}
