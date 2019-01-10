set(BINARY_SOURCES
        logmf.c
        )

# Add an executable with the above sources
add_executable(AprofLogger ${BINARY_SOURCES})

# link the new hello_library target with the hello_binary target
target_link_libraries(AprofLogger m rt)