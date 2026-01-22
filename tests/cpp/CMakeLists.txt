cmake_minimum_required(VERSION 3.16)

project(aptos-sdk-spec-tests-cpp LANGUAGES CXX)

# CWT-Cucumber requires C++20
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Export compile commands for IDE support
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# =============================================================================
# Dependencies
# =============================================================================

# Option 1: Use Conan (recommended)
# Run: conan install . --output-folder=build --build=missing
if(EXISTS "${CMAKE_BINARY_DIR}/conan_toolchain.cmake")
    include("${CMAKE_BINARY_DIR}/conan_toolchain.cmake")
endif()

# Find CWT-Cucumber
find_package(cwt-cucumber QUIET)
if(NOT cwt-cucumber_FOUND)
    # Option 2: FetchContent fallback
    include(FetchContent)
    FetchContent_Declare(
        cwt-cucumber
        GIT_REPOSITORY https://github.com/ThoSe1990/cwt-cucumber.git
        GIT_TAG 2.8
    )
    FetchContent_MakeAvailable(cwt-cucumber)
endif()

# JSON library for test vectors
find_package(nlohmann_json QUIET)
if(NOT nlohmann_json_FOUND)
    include(FetchContent)
    FetchContent_Declare(
        nlohmann_json
        GIT_REPOSITORY https://github.com/nlohmann/json.git
        GIT_TAG v3.11.3
    )
    FetchContent_MakeAvailable(nlohmann_json)
endif()

# =============================================================================
# Aptos C++ SDK (Built by Var Meta)
# =============================================================================
# Repository: https://github.com/VAR-META-Tech/Aptos-Cpp-SDK
# Documentation: https://aptos.dev/build/sdks/cpp-sdk
#
# NOTE: The SDK has complex dependencies (bip3x, cryptopp, cpprestsdk) and 
# requires Conan for dependency management. Integration requires:
# 1. Clone the SDK separately
# 2. Build it following their instructions
# 3. Link against the built libraries
#
# For simpler testing, we use placeholder types that allow the test scaffold
# to compile and run without the full SDK dependency chain.

# -----------------------------------------------------------------------------
# Option A: Local path (recommended for development)
# -----------------------------------------------------------------------------
# First, clone and build the SDK:
#   git clone https://github.com/VAR-META-Tech/Aptos-Cpp-SDK.git
#   cd Aptos-Cpp-SDK
#   git submodule update --init --recursive
#   conan install . -s compiler.cppstd=20 --build=missing
#   cd build && cmake .. && make
#
# Then set the path here:
# set(APTOS_CPP_SDK_PATH "/path/to/Aptos-Cpp-SDK")
# if(EXISTS "${APTOS_CPP_SDK_PATH}/Src")
#     target_include_directories(aptos_spec_tests PRIVATE ${APTOS_CPP_SDK_PATH}/Src)
#     target_link_directories(aptos_spec_tests PRIVATE ${APTOS_CPP_SDK_PATH}/build)
#     target_link_libraries(aptos_spec_tests PRIVATE Aptos)
#     set(APTOS_SDK_AVAILABLE TRUE)
# endif()

# -----------------------------------------------------------------------------
# Option B: FetchContent (requires handling SDK's dependencies)
# -----------------------------------------------------------------------------
# The SDK uses git submodules and Conan, so FetchContent alone won't work.
# You'd need to also fetch bip3x, cryptopp, cpprestsdk, toolbox.

# For now, we build without the SDK (placeholder types in world.hpp)
set(APTOS_SDK_AVAILABLE FALSE)

if(NOT APTOS_SDK_AVAILABLE)
    message(STATUS "Building without Aptos C++ SDK - using placeholder types")
    message(STATUS "SDK repo: https://github.com/VAR-META-Tech/Aptos-Cpp-SDK")
endif()

# =============================================================================
# Test Executable
# =============================================================================

# Collect source files
set(SUPPORT_SOURCES
    support/vectors.cpp
    support/placeholders.cpp
)

set(STEP_SOURCES
    steps/address_steps.cpp
    steps/cryptography_steps.cpp
    steps/serialization_steps.cpp
    steps/hashing_steps.cpp
    steps/account_steps.cpp
    steps/transaction_steps.cpp
)

# Main test executable
add_executable(aptos_spec_tests
    src/main.cpp
    ${SUPPORT_SOURCES}
    ${STEP_SOURCES}
)

target_include_directories(aptos_spec_tests PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/support
    ${CMAKE_CURRENT_SOURCE_DIR}/steps
)

# Link dependencies
target_link_libraries(aptos_spec_tests PRIVATE
    cwt::cucumber
    nlohmann_json::nlohmann_json
)

# Conditionally link SDK when available
if(APTOS_SDK_AVAILABLE)
    target_link_libraries(aptos_spec_tests PRIVATE aptos-cpp-sdk::aptos-cpp-sdk)
    target_compile_definitions(aptos_spec_tests PRIVATE APTOS_SDK_AVAILABLE=1)
endif()

# =============================================================================
# Testing
# =============================================================================

enable_testing()

# Features directory (relative to build dir when running tests)
set(FEATURES_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../../features")

# All tests
add_test(
    NAME all_specs
    COMMAND aptos_spec_tests "${FEATURES_DIR}"
)

# Required tests only (P0)
add_test(
    NAME required_specs
    COMMAND aptos_spec_tests "${FEATURES_DIR}" --tags "@required"
)

# Preferred tests (P1)
add_test(
    NAME preferred_specs
    COMMAND aptos_spec_tests "${FEATURES_DIR}" --tags "@preferred"
)

# Category-specific tests
add_test(
    NAME core_types_specs
    COMMAND aptos_spec_tests "${FEATURES_DIR}" --tags "@core-types"
)

add_test(
    NAME cryptography_specs
    COMMAND aptos_spec_tests "${FEATURES_DIR}" --tags "@cryptography"
)

add_test(
    NAME accounts_specs
    COMMAND aptos_spec_tests "${FEATURES_DIR}" --tags "@accounts"
)

add_test(
    NAME transactions_specs
    COMMAND aptos_spec_tests "${FEATURES_DIR}" --tags "@transactions"
)
