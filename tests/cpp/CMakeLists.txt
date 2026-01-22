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
# The SDK is cloned locally in the `sdk/` directory and built with Conan.

set(APTOS_CPP_SDK_PATH "${CMAKE_CURRENT_SOURCE_DIR}/sdk")

if(EXISTS "${APTOS_CPP_SDK_PATH}/Src" AND EXISTS "${APTOS_CPP_SDK_PATH}/build/build/Release/libAptos.dylib")
    set(APTOS_SDK_AVAILABLE TRUE)
    message(STATUS "Found Aptos C++ SDK at: ${APTOS_CPP_SDK_PATH}")
    
    # Set CMAKE_PREFIX_PATH to find SDK's dependencies via Conan
    set(SDK_CONAN_DIR "${APTOS_CPP_SDK_PATH}/build/build/Release/generators")
    if(EXISTS "${SDK_CONAN_DIR}")
        list(APPEND CMAKE_PREFIX_PATH "${SDK_CONAN_DIR}")
        message(STATUS "Added SDK Conan generators to CMAKE_PREFIX_PATH: ${SDK_CONAN_DIR}")
    endif()
    
    # Find SDK's dependencies (installed via Conan)
    find_package(cryptopp REQUIRED)
    find_package(cpprestsdk QUIET)
    find_package(Boost QUIET)
    find_package(OpenSSL QUIET)
else()
    set(APTOS_SDK_AVAILABLE FALSE)
    message(STATUS "Aptos C++ SDK not found - using placeholder types")
    message(STATUS "To build the SDK:")
    message(STATUS "  cd ${APTOS_CPP_SDK_PATH}")
    message(STATUS "  conan install . -s compiler.cppstd=20 --build=missing --output-folder=build")
    message(STATUS "  cd build && cmake .. --preset conan-release")
    message(STATUS "  cd build/Release && make Aptos")
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

# Conditionally add SDK includes and link libraries
if(APTOS_SDK_AVAILABLE)
    set(SDK_BUILD_DIR "${APTOS_CPP_SDK_PATH}/build/build/Release")
    
    # SDK source headers
    target_include_directories(aptos_spec_tests PRIVATE
        ${APTOS_CPP_SDK_PATH}/Src
        ${APTOS_CPP_SDK_PATH}/ThirdParty/bip3x/include
        ${SDK_BUILD_DIR}/_deps/toolbox-src/include
    )
    
    target_link_directories(aptos_spec_tests PRIVATE
        ${SDK_BUILD_DIR}
    )
    
    target_compile_definitions(aptos_spec_tests PRIVATE APTOS_SDK_AVAILABLE=1)
endif()

# Link dependencies
target_link_libraries(aptos_spec_tests PRIVATE
    cwt::cucumber
    nlohmann_json::nlohmann_json
)

# Conditionally link SDK when available
if(APTOS_SDK_AVAILABLE)
    target_link_libraries(aptos_spec_tests PRIVATE
        Aptos
    )
    
    # Link SDK's dependencies if found
    if(cryptopp_FOUND)
        target_link_libraries(aptos_spec_tests PRIVATE cryptopp::cryptopp)
    endif()
    if(cpprestsdk_FOUND)
        target_link_libraries(aptos_spec_tests PRIVATE cpprestsdk::cpprestsdk)
    endif()
    if(Boost_FOUND)
        target_link_libraries(aptos_spec_tests PRIVATE Boost::boost)
    endif()
    if(OpenSSL_FOUND)
        target_link_libraries(aptos_spec_tests PRIVATE OpenSSL::SSL OpenSSL::Crypto)
    endif()
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
