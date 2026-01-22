plugins {
    kotlin("jvm") version "1.9.22"
}

group = "com.aptos"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    // Kaptos SDK - Kotlin Multiplatform SDK for Aptos (published to Maven Central)
    // Use the JVM-specific artifact for pure JVM testing
    implementation("xyz.mcxross.kaptos:kaptos-jvm:0.1.2-beta")
    
    // Cucumber BDD Framework
    testImplementation("io.cucumber:cucumber-java:7.15.0")
    testImplementation("io.cucumber:cucumber-junit-platform-engine:7.15.0")
    testImplementation("io.cucumber:cucumber-picocontainer:7.15.0")
    
    // JUnit 5 Platform
    testImplementation("org.junit.platform:junit-platform-suite:1.10.1")
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.1")
    
    // JSON parsing for test vectors
    testImplementation("com.google.code.gson:gson:2.10.1")
    
    // Kotlin coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
    
    // Kotest assertions
    testImplementation("io.kotest:kotest-assertions-core:5.8.0")
}

kotlin {
    jvmToolchain(17)
}

tasks.test {
    useJUnitPlatform()
    
    systemProperty("cucumber.junit-platform.naming-strategy", "long")
    systemProperty("cucumber.plugin", "pretty,html:build/reports/cucumber/cucumber.html,json:build/reports/cucumber/cucumber.json")
    systemProperty("cucumber.features", "../../features")
    systemProperty("cucumber.glue", "com.aptos.specs.steps,com.aptos.specs.support")
    
    // Pass through tag filter from command line
    systemProperty("cucumber.filter.tags", System.getProperty("cucumber.filter.tags") ?: "")
}

// Task for running only required tests
tasks.register<Test>("testRequired") {
    useJUnitPlatform()
    systemProperty("cucumber.filter.tags", "@required")
    systemProperty("cucumber.features", "../../features")
    systemProperty("cucumber.glue", "com.aptos.specs.steps,com.aptos.specs.support")
}

// Task for running only preferred tests
tasks.register<Test>("testPreferred") {
    useJUnitPlatform()
    systemProperty("cucumber.filter.tags", "@preferred")
    systemProperty("cucumber.features", "../../features")
    systemProperty("cucumber.glue", "com.aptos.specs.steps,com.aptos.specs.support")
}

// Task for running core-types tests
tasks.register<Test>("testCoreTypes") {
    useJUnitPlatform()
    systemProperty("cucumber.filter.tags", "@core-types")
    systemProperty("cucumber.features", "../../features")
    systemProperty("cucumber.glue", "com.aptos.specs.steps,com.aptos.specs.support")
}

// Task for running cryptography tests
tasks.register<Test>("testCryptography") {
    useJUnitPlatform()
    systemProperty("cucumber.filter.tags", "@cryptography")
    systemProperty("cucumber.features", "../../features")
    systemProperty("cucumber.glue", "com.aptos.specs.steps,com.aptos.specs.support")
}

// Task for running transaction tests
tasks.register<Test>("testTransactions") {
    useJUnitPlatform()
    systemProperty("cucumber.filter.tags", "@transactions")
    systemProperty("cucumber.features", "../../features")
    systemProperty("cucumber.glue", "com.aptos.specs.steps,com.aptos.specs.support")
}

// Dry run task
tasks.register<Test>("dryRun") {
    useJUnitPlatform()
    systemProperty("cucumber.execution.dry-run", "true")
    systemProperty("cucumber.features", "../../features")
    systemProperty("cucumber.glue", "com.aptos.specs.steps,com.aptos.specs.support")
}
