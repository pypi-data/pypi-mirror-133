cmake_minimum_required(VERSION 3.10)
project(MapRenderCache)

set(CMAKE_CXX_STANDARD 17)

find_package(pybind11 CONFIG REQUIRED)

execute_process(COMMAND python3 -m site --user-site OUTPUT_VARIABLE PYTHON_SITE OUTPUT_STRIP_TRAILING_WHITESPACE)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

pybind11_add_module(MapRenderCache python_bindings.cpp)
target_link_libraries(MapRenderCache PUBLIC mapnik icuuc)

set_target_properties(MapRenderCache PROPERTIES PUBLIC_HEADER "MapRenderCache.h")

install(TARGETS MapRenderCache
        DESTINATION ${PYTHON_SITE}
        PUBLIC_HEADER DESTINATION MapRenderCache
        )
