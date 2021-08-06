cmake_minimum_required(VERSION 3.21.1)

project(${PROJECT_NAME} LANGUAGES CXX)

set(SFML_DIR ${CMAKE_CURRENT_SOURCE_DIR}/lib/cmake/SFML)
set(TGUI_DIR ${CMAKE_CURRENT_SOURCE_DIR}/lib/cmake/TGUI)
set(SFML_STATIC_LIBRARIES TRUE)
set(TGUI_STATIC_LIBRARIES TRUE)

find_package(SFML 2.5.1 COMPONENTS system window graphics)
find_package(TGUI)

file(GLOB SOURCES src/*.cpp)

add_executable(main ${SOURCES})

target_link_libraries(main sfml-system sfml-window sfml-graphics tgui)
